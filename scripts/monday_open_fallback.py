#!/usr/bin/env python3
"""Independent, append-only Monday opening observations. Does not touch the primary tape."""

import argparse
import base64
import fcntl
import gzip
import hashlib
import hmac
import json
import os
import secrets
import signal
import subprocess
import sys
import tempfile
import time
from decimal import Decimal, DecimalException
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.server import NoRedirect, binance_credentials

BASE = "https://web3.binance.com/build"
TOKENS = "/api/v1/dex/market/rwa/tokens"
PRICE = "/api/v1/dex/market/rwa/price"
LOCAL = ROOT / "data/monday_open_fallback/local"
PREFLIGHT = ROOT / "data/monday_open_fallback/local/PREFLIGHT"
MONDAY = ROOT / "data/monday_open_fallback/local/MONDAY"
MARKET = ROOT / "data/market_hours"
START = datetime(2026, 10, 5, 13, 20, tzinfo=timezone.utc).timestamp()
END = datetime(2026, 10, 5, 13, 45, tzinfo=timezone.utc).timestamp()
CONTRACTS = [
 ("NVDA","bstock","0x02fca66c1d1afb4e2a7884261eb00f63598a7436"),
 ("NVDA","ondo","0xa9ee28c80f960b889dfbd1902055218cba016f75"),
 ("TSLA","bstock","0x5b1910eaad6450e50f816082aa078c41f10c292f"),
 ("TSLA","ondo","0x2494b603319d4d9f9715c9f4496d9e0364b59d93"),
 ("COIN","bstock","0x585bde7c54abb5ccd7791f923d6c2187635f3952"),
 ("COIN","ondo","0xf8589b526fdd65f7f301c605a6e04f0f1b4b3620"),
]

def now(): return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")
def read(path):
    try: return json.loads(path.read_text())
    except (OSError, ValueError): return {}
def last_jsonl(path):
    try:
        lines=path.read_text(encoding="utf-8").splitlines()
        return json.loads(lines[-1]) if lines else {}
    except (OSError,ValueError): return {}
def append(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd=os.open(str(path),os.O_CREAT|os.O_WRONLY|os.O_APPEND,0o600)
    try:
        os.write(fd,(json.dumps(row,separators=(",",":"),sort_keys=True)+"\n").encode()); os.fsync(fd)
    finally: os.close(fd)
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n"); os.replace(tmp,path)
def process_alive(pid, fragment):
    if not isinstance(pid,int) or pid < 1: return False
    p=subprocess.run(["ps","-p",str(pid),"-o","command="],capture_output=True,text=True,timeout=5)
    return p.returncode==0 and fragment in p.stdout
def primary_health():
    hb=read(MARKET/"heartbeat.json"); wh=read(MARKET/"underlying_market_watch_health.json")
    try: pid=int((MARKET/"collector.pid").read_text().strip())
    except (OSError,ValueError): pid=None
    try: wpid=int((MARKET/"watchdog.pid").read_text().strip())
    except (OSError,ValueError): wpid=None
    collector=process_alive(pid,"rwa_research.py")
    watchdog=process_alive(wpid,"collector_watchdog.py")
    by_slot={}
    for path in sorted(MARKET.glob("20??-??-??.jsonl"))[-2:]:
        try:
            with path.open(encoding="utf-8") as stream:
                for line in stream:
                    try: row=json.loads(line)
                    except ValueError: continue
                    if row.get("origin")=="LIVE" and isinstance(row.get("slot"),int) and row.get("contract"):
                        entry=by_slot.setdefault(row["slot"],{})
                        entry[row["contract"].lower()]=row.get("observed_at")
        except OSError: continue
    complete_slots=[s for s,contracts in by_slot.items() if len(contracts)==40]
    slot=max(complete_slots) if complete_slots else None
    complete=slot is not None
    latest=datetime.fromtimestamp(slot*300,timezone.utc).isoformat().replace("+00:00","Z") if isinstance(slot,int) else None
    underlying=wh.get("last_success_at")
    try: age=max(0,int(time.time()-datetime.fromisoformat(underlying.replace("Z","+00:00")).timestamp()))
    except (AttributeError,ValueError): age=None
    stamp=max((x for x in by_slot.get(slot,{}).values() if x),default=None) if slot is not None else None
    try: primary_age=max(0,int(time.time()-datetime.fromisoformat(stamp.replace("Z","+00:00")).timestamp()))
    except (AttributeError,ValueError): primary_age=None
    return {"primary_source":"PRIMARY","fallback_source":"FALLBACK","collector_pid_alive":collector,"watchdog_alive":watchdog,"latest_complete_slot":slot if complete else None,
      "latest_complete_slot_started_at":latest if complete else None,"underlying_watch_last_success":underlying,
      "current_utc":now(),"seconds_since_last_successful_observation":primary_age,
      "underlying_watch_age_seconds":age}

def save_raw(folder, endpoint, body, observed_at):
    if len(body)>2_000_000: raise RuntimeError("response exceeds 2 MB guard")
    digest=hashlib.sha256(body).hexdigest(); raw=folder/"raw"; raw.mkdir(parents=True,exist_ok=True)
    target=raw/(digest+".json.gz")
    if not target.exists():
        with tempfile.NamedTemporaryFile(dir=raw,delete=False) as f: temp=Path(f.name)
        try:
            with gzip.open(temp,"wb") as f: f.write(body)
            os.replace(temp,target)
        finally: temp.unlink(missing_ok=True)
    append(folder/"raw-manifest.jsonl",{"origin":"FALLBACK","captured_at":observed_at,"endpoint":endpoint,"sha256":digest,"path":str(target)})
    return digest

class SignedApi:
    def __init__(self):
        auth=binance_credentials(ROOT)
        if not auth: raise RuntimeError("Binance Web3 credentials unavailable")
        self.key,self.secret=auth
    def get(self,path,params,folder):
        q=urlencode(params); at=now(); signed="/build"+path+("?"+q if q else "")
        sig=base64.b64encode(hmac.new(self.secret.encode(),(at+"GET"+signed).encode(),hashlib.sha256).digest()).decode()
        req=Request(BASE+path+("?"+q if q else ""),headers={"X-OC-APIKEY":self.key,"X-OC-TIMESTAMP":at,"X-OC-SIGN":sig,
          "X-OC-NONCE":secrets.token_hex(16),"Accept":"application/json"},method="GET")
        status=None; body=b""; err=None; retry=None
        try:
            with build_opener(NoRedirect()).open(req,timeout=15) as r:
                status=r.status
                if r.geturl()!=req.full_url: raise RuntimeError("redirect rejected")
                body=r.read(2_000_001)
        except HTTPError as e: status=e.code; retry=e.headers.get("Retry-After"); body=e.read(2_000_001)
        except (URLError,TimeoutError,OSError) as e: err=type(e).__name__
        received=now()
        if self.key.encode() in body or self.secret.encode() in body: raise RuntimeError("secret scan rejected raw body")
        digest=save_raw(folder,path,body,received) if body else None
        payload={}
        try: payload=json.loads(body)
        except (ValueError,UnicodeDecodeError): err=err or "invalid_json"
        good=status==200 and isinstance(payload,dict) and payload.get("code")==0 and isinstance(payload.get("data"),list)
        if not good:
            raise ApiFailure("API response invalid (HTTP %s; %s)"%(status,err or "business/schema error"),retry,status,payload.get("code") if isinstance(payload,dict) else None)
        return payload,received,digest

class ApiFailure(RuntimeError):
    def __init__(self,msg,retry=None,status=None,code=None): super().__init__(msg); self.retry=retry; self.status=status; self.code=code

def capture_local(folder,label,scheduled_at=None):
    if scheduled_at:
        oid=hashlib.sha256(scheduled_at.encode()).hexdigest()[:24]
        try:
            if any(json.loads(line).get("observation_id")==oid for line in (folder/"slots.jsonl").read_text().splitlines()):
                return {"origin":"FALLBACK","mode":label,"observation_id":oid,"duplicate_skipped":True}
        except (OSError,ValueError): pass
    api=SignedApi(); begun=now(); rows=[]; errs=[]
    try:
        catalog,cat_at,cat_hash=api.get(TOKENS,[("binanceChainId","56")],folder)
        by={str(x.get("tokenContractAddress","")).lower():x for x in catalog["data"] if isinstance(x,dict)}
        for ticker,provider,address in CONTRACTS:
            item=by.get(address)
            if (not item or str(item.get("binanceChainId"))!="56" or item.get("underlyingTicker")!=ticker
                    or str(item.get("assetType"))!="1" or str(item.get("platformId")).lower()!=provider):
                raise RuntimeError("fixed contract catalog identity, BSC chain, asset type, ticker, or provider mismatch: %s/%s"%(ticker,provider))
        addr_list=",".join(address for _,_,address in CONTRACTS)
        p,at,digest=api.get(PRICE,[("binanceChainId","56"),("tokenContractAddresses",addr_list)],folder)
        price_rows=p["data"]
        price_by={str(x.get("tokenContractAddress","")).lower():x for x in price_rows if isinstance(x,dict)}
        if set(price_by)!=set(a for _,_,a in CONTRACTS): raise RuntimeError("batch price response did not contain exactly the six requested identities")
        for ticker,provider,address in CONTRACTS:
            item=by[address]; price=price_by[address]
            if str(price.get("tokenContractAddress","")).lower()!=address:
                raise RuntimeError("batch price response identity mismatch")
            price_chain_validation="verified_56" if str(price.get("binanceChainId"))=="56" else "not_returned_by_price_endpoint"
            if price.get("binanceChainId") is not None and str(price.get("binanceChainId"))!="56": raise RuntimeError("batch price response wrong chain")
            ratio=item.get("tokenToShareRatio"); token_price=price.get("tokenPrice")
            try: per=str(Decimal(str(token_price))/Decimal(str(ratio))) if token_price is not None and ratio is not None else None
            except DecimalException: per=None
            oid=hashlib.sha256(((scheduled_at or begun)+address).encode()).hexdigest()[:24]
            if observation_exists(folder,oid): continue
            rows.append({"origin":"FALLBACK","mode":label,"observation_id":oid,"scheduled_at":scheduled_at,"observed_at":at,"catalog_observed_at":cat_at,
              "provider":provider,"ticker":ticker,"chain_id":"56","contract":address,
              "token_price_usd":token_price,"token_price_updated_at_ms":price.get("tokenPriceUpdatedAt"),
              "price_response_chain_validation":price_chain_validation,
              "token_to_share_ratio":ratio,"token_derived_per_share_usd":per,
              "reference_price_usd":price.get("referencePrice"),"reference_price_updated_at":None,
              "reference_age_seconds":None,"reference_age_status":"UNKNOWN",
              "catalog_response_sha256":cat_hash,"price_response_sha256":digest})
    except Exception as e:
        errs.append({"origin":"FALLBACK","mode":label,"at":now(),"error_type":type(e).__name__,"message":str(e)[:240]})
        append(folder/"errors.jsonl",errs[-1]); raise
    existing=set()
    try:
        for line in (folder/"slots.jsonl").read_text().splitlines(): existing.add(json.loads(line).get("observation_id"))
    except (OSError,ValueError): pass
    oid=hashlib.sha256((scheduled_at or begun).encode()).hexdigest()[:24]
    if oid in existing: return {"origin":"FALLBACK","mode":label,"observation_id":oid,"duplicate_skipped":True}
    for row in rows: append(folder/"observations.jsonl",row)
    expected_ids={hashlib.sha256(((scheduled_at or begun)+address).encode()).hexdigest()[:24] for _,_,address in CONTRACTS}
    sampled=sum(1 for observation_id in expected_ids if observation_exists(folder,observation_id))
    slot={"origin":"FALLBACK","mode":label,"observation_id":oid,"scheduled_at":scheduled_at,"started_at":begun,"completed_at":now(),"contracts_expected":6,"contracts_sampled":sampled,"complete":sampled==6}
    append(folder/"slots.jsonl",slot); return slot

def yahoo_once(folder,label,scheduled_at=None):
    successes=0; slot=scheduled_at or now(); rate_limit=None
    for ticker in ("NVDA","TSLA","COIN"):
        url="https://query1.finance.yahoo.com/v8/finance/chart/%s?range=1d&interval=1m"%ticker
        req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        try:
            with build_opener(NoRedirect()).open(req,timeout=12) as r:
                if r.status!=200 or r.geturl().split("?")[0]!=url.split("?")[0]: raise RuntimeError("Yahoo status/redirect rejected")
                body=r.read(2_000_001)
            if len(body)>2_000_000: raise RuntimeError("Yahoo response exceeds 2 MB guard")
            at=now(); digest=save_raw(folder,"yahoo_chart:"+ticker,body,at); payload=json.loads(body)
            result=payload.get("chart",{}).get("result") or []
            if not result: raise RuntimeError("Yahoo returned no chart result")
            row=result[0]; meta=row.get("meta",{}); q=((row.get("indicators",{}).get("quote") or [{}])[0])
            timestamps=row.get("timestamp") or []; opens=q.get("open") or []; closes=q.get("close") or []
            latest=next((i for i in range(min(len(timestamps),len(closes))-1,-1,-1) if closes[i] is not None),None)
            regular=meta.get("currentTradingPeriod",{}).get("regular",{}) if isinstance(meta.get("currentTradingPeriod"),dict) else {}
            first_regular=next((i for i,stamp in enumerate(timestamps) if stamp>=regular.get("start",float("inf")) and stamp<regular.get("end",float("-inf")) and i<len(opens) and opens[i] is not None),None)
            oid=hashlib.sha256((slot+ticker).encode()).hexdigest()[:24]
            successes+=1
            if observation_exists(folder,oid): continue
            append(folder/"observations.jsonl",{"origin":"FALLBACK","mode":label,"observation_id":oid,"scheduled_at":scheduled_at,"ticker":ticker,"observed_at":at,
              "source":"Yahoo Finance chart API","source_url":url,"status":"INTRADAY_SUPPORTING_ONLY",
              "latest_bar_timestamp":timestamps[latest] if latest is not None else None,
              "latest_bar_open_usd":opens[latest] if latest is not None and latest<len(opens) else None,
              "latest_bar_close_usd":closes[latest] if latest is not None else None,
              "first_regular_session_bar_timestamp":timestamps[first_regular] if first_regular is not None else None,
              "first_regular_session_bar_open_usd":opens[first_regular] if first_regular is not None else None,
              "first_regular_session_bar_type":"intraday chart bar; not a historical daily open" if first_regular is not None else None,
              "regular_session_boundary_source":"Yahoo chart meta currentTradingPeriod.regular" if regular else None,
              "currency":meta.get("currency"),"raw_response_sha256":digest,
              "reference_price_updated_at":None,"reference_age_status":"UNKNOWN"})
        except HTTPError as e:
            body=e.read(2_000_001); at=now()
            if body and len(body)<=2_000_000: save_raw(folder,"yahoo_chart_error:"+ticker,body,at)
            append(folder/"errors.jsonl",{"origin":"FALLBACK","mode":label,"ticker":ticker,"at":at,"error_type":"HTTPError","http_status":e.code,"retry_after":e.headers.get("Retry-After"),"message":"Yahoo chart HTTP failure; raw body retained when bounded"})
            if e.code==429: rate_limit=e.headers.get("Retry-After","")
        except Exception as e: append(folder/"errors.jsonl",{"origin":"FALLBACK","mode":label,"ticker":ticker,"at":now(),"error_type":type(e).__name__,"message":str(e)[:200]})
    if rate_limit is not None: raise ApiFailure("Yahoo HTTP 429",rate_limit,429)
    return successes

def observation_exists(folder,oid):
    try:
        with (folder/"observations.jsonl").open(encoding="utf-8") as stream:
            return any(json.loads(line).get("observation_id")==oid for line in stream if line.strip())
    except OSError: return False
def record_exists(path,field,value):
    try:
        with path.open(encoding="utf-8") as stream:
            return any(json.loads(line).get(field)==value for line in stream if line.strip())
    except OSError: return False

def public_dynamic(folder,scheduled_at,label="MONDAY"):
    base="https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai"
    count=0; rate_limit=None
    for ticker,provider,address in CONTRACTS:
        url=base+"?"+urlencode({"chainId":"56","contractAddress":address})
        req=Request(url,headers={"Accept-Encoding":"identity","Accept":"application/json","User-Agent":"binance-web3/1.1 (read-only fallback)"})
        try:
            with build_opener(NoRedirect()).open(req,timeout=15) as response:
                if response.status!=200 or response.geturl()!=url: raise RuntimeError("public dynamic HTTP/redirect failure")
                body=response.read(100_001)
            if len(body)>100_000: raise RuntimeError("public dynamic response exceeds size guard")
            at=now(); digest=save_raw(folder,"binance_public_dynamic:"+address,body,at); payload=json.loads(body)
            if not isinstance(payload,dict) or payload.get("code")!="000000" or not isinstance(payload.get("data"),dict): raise RuntimeError("public dynamic response schema/business code invalid")
            data=payload["data"]; token=data.get("tokenInfo") if isinstance(data.get("tokenInfo"),dict) else {}
            stock=data.get("stockInfo") if isinstance(data.get("stockInfo"),dict) else {}
            response_contract=token.get("contractAddress") or data.get("contractAddress")
            response_chain=token.get("chainId") or data.get("chainId")
            response_ticker=data.get("ticker") or token.get("ticker") or stock.get("ticker")
            if response_contract is not None and str(response_contract).lower()!=address: raise RuntimeError("public dynamic response contract mismatch")
            if response_chain is not None and str(response_chain)!="56": raise RuntimeError("public dynamic response chain mismatch")
            if response_ticker is not None and str(response_ticker).upper()!=ticker: raise RuntimeError("public dynamic response ticker mismatch")
            oid=hashlib.sha256((label+scheduled_at+"binance-public:"+address).encode()).hexdigest()[:24]
            if not observation_exists(folder,oid):
                append(folder/"observations.jsonl",{"origin":"FALLBACK","mode":label,"observation_id":oid,"scheduled_at":scheduled_at,
                  "observed_at":at,"source":"BINANCE_PUBLIC_DYNAMIC","source_url":url,"ticker":ticker,"provider":provider,
                  "contract":address,"chain_id":"56","token_price":token.get("price"),"token_price_status":"VALUE_PRESENT" if token.get("price") is not None else "NULL_OR_UNAVAILABLE","stock_reference_price":stock.get("price"),
                  "response_contract_address":response_contract,"response_chain_id":response_chain,"response_ticker":response_ticker,
                  "response_identity_validation":{"contract":"verified" if response_contract is not None else "not_returned","chain":"verified" if response_chain is not None else "query_parameter_56_only","ticker":"verified" if response_ticker is not None else "not_returned"},
                  "token_price_updated_at":None,"stock_reference_updated_at":None,"reference_age_status":"UNKNOWN",
                  "stock_reference_status":"VALUE_PRESENT" if stock.get("price") is not None else "NULL_OR_UNAVAILABLE",
                  "unsupported_fields":(["stockInfo.price"] if "price" not in stock else []),"raw_response_sha256":digest,
                  "provenance":"credential-free website BAPI; not signed Web3 API; supporting fallback only"})
            if token.get("price") is not None: count+=1
            else: append(folder/"errors.jsonl",{"origin":"FALLBACK","scheduled_at":scheduled_at,"at":at,"source":"BINANCE_PUBLIC_DYNAMIC","ticker":ticker,"provider":provider,"contract":address,"error_type":"missing_token_price","message":"raw response retained; tokenInfo.price unavailable"})
        except HTTPError as e:
            body=e.read(100_001); at=now()
            if body and len(body)<=100_000: save_raw(folder,"binance_public_dynamic_error:"+address,body,at)
            append(folder/"errors.jsonl",{"origin":"FALLBACK","scheduled_at":scheduled_at,"at":at,"source":"BINANCE_PUBLIC_DYNAMIC","ticker":ticker,"provider":provider,"contract":address,"http_status":e.code,"retry_after":e.headers.get("Retry-After"),"message":"public dynamic HTTP failure; bounded body retained"})
            if e.code==429: rate_limit=e.headers.get("Retry-After","")
        except Exception as e: append(folder/"errors.jsonl",{"origin":"FALLBACK","scheduled_at":scheduled_at,"at":now(),"source":"BINANCE_PUBLIC_DYNAMIC","ticker":ticker,"provider":provider,"contract":address,"error_type":type(e).__name__,"message":str(e)[:200]})
    if rate_limit is not None: raise ApiFailure("public dynamic HTTP 429",rate_limit,429)
    return count

def yahoo_close(folder):
    # A short daily chart range is retained only as dated historical support;
    # this mode never writes scorer input and never supplies a reference clock.
    found=0
    for ticker in ("NVDA","TSLA","COIN"):
        url="https://query1.finance.yahoo.com/v8/finance/chart/%s?range=5d&interval=1d"%ticker
        req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
        try:
            with build_opener(NoRedirect()).open(req,timeout=15) as r:
                if r.status!=200 or r.geturl().split("?")[0]!=url.split("?")[0]: raise RuntimeError("Yahoo status/redirect rejected")
                body=r.read(2_000_001)
            if len(body)>2_000_000: raise RuntimeError("Yahoo response exceeds 2 MB guard")
            at=now(); digest=save_raw(folder,"yahoo_daily_chart:"+ticker,body,at); payload=json.loads(body)
            chart=payload.get("chart",{}); result=chart.get("result") or []; row=result[0] if result else {}
            timestamps=row.get("timestamp") or []; quote=((row.get("indicators",{}).get("quote") or [{}])[0])
            meta=row.get("meta",{}); tz=timezone.utc
            try:
                from zoneinfo import ZoneInfo
                tz=ZoneInfo(meta.get("exchangeTimezoneName") or "UTC")
            except Exception: pass
            selected=None
            for i,stamp in enumerate(timestamps):
                session=datetime.fromtimestamp(stamp,tz).date().isoformat()
                if session=="2026-10-05": selected={"session_date":session,
                    "open_usd":(quote.get("open") or [])[i] if i<len(quote.get("open") or []) else None,
                    "close_usd":(quote.get("close") or [])[i] if i<len(quote.get("close") or []) else None}
            if selected and selected.get("open_usd") is not None: found+=1
            append(folder/"observations.jsonl",{"origin":"FALLBACK","mode":"MONDAY_CLOSE_SUPPORTING_ONLY","ticker":ticker,
              "observed_at":at,"source":"Yahoo Finance chart API","source_url":url,"session_row":selected,
              "session_row_status":"ROW_FOUND" if selected else "ROW_UNAVAILABLE","currency":meta.get("currency"),
              "raw_response_sha256":digest,"reference_price_updated_at":None,"reference_age_status":"UNKNOWN"})
        except HTTPError as e:
            body=e.read(2_000_001); at=now()
            if body and len(body)<=2_000_000: save_raw(folder,"yahoo_daily_chart_error:"+ticker,body,at)
            append(folder/"errors.jsonl",{"origin":"FALLBACK","mode":"MONDAY_CLOSE_SUPPORTING_ONLY","ticker":ticker,"at":at,"error_type":"HTTPError","http_status":e.code,"retry_after":e.headers.get("Retry-After"),"message":"Yahoo chart HTTP failure; raw body retained when bounded"})
        except Exception as e: append(folder/"errors.jsonl",{"origin":"FALLBACK","mode":"MONDAY_CLOSE_SUPPORTING_ONLY","ticker":ticker,"at":now(),"error_type":type(e).__name__,"message":str(e)[:200]})
    return found

def slot_text(epoch): return datetime.fromtimestamp(epoch,timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
def record_gap(folder, start_epoch, end_epoch, reason):
    gid=hashlib.sha256((str(start_epoch)+":"+str(end_epoch)+":"+reason).encode()).hexdigest()[:24]
    if record_exists(folder/"gaps.jsonl","gap_id",gid): return
    append(folder/"gaps.jsonl",{"origin":"FALLBACK","gap_id":gid,"from_scheduled_at":slot_text(start_epoch),"through_scheduled_at":slot_text(end_epoch),"reason":reason,"recorded_at":now()})

def loop(public=False):
    folder=(Path(os.environ.get("MONDAY_FALLBACK_OUTPUT_DIR",str(ROOT/"data/monday_open_fallback/public")))/"MONDAY") if public else MONDAY
    folder.mkdir(parents=True,exist_ok=True); lock=os.open(str(folder/".lock"),os.O_CREAT|os.O_RDWR,0o600)
    try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError: raise SystemExit("fallback process already running")
    atomic(folder/"pid.json",{"pid":os.getpid(),"started_at":now(),"mode":"PUBLIC" if public else "LOCAL"})
    previous=None
    current=time.time(); next_capture=max(START,(int((current+59)//60))*60)
    if next_capture>START: record_gap(folder,START,next_capture-60,"process_started_after_slot_boundary; no backfill")
    next_health=max(START,current)
    cooldown=read(folder/"backoff.json").get("not_before_epoch",0)
    slot_success={}
    while time.time()<END:
        t=time.time()
        if t>=START:
            if t>=next_capture:
                scheduled=next_capture; stamp=slot_text(scheduled)
                cooldown=max(cooldown,read(folder/"backoff.json").get("not_before_epoch",0))
                if t<cooldown:
                    record_gap(folder,scheduled,scheduled,"rate_limit_backoff; no request")
                else:
                    try:
                        if public:
                            slot_success[stamp]={"yahoo":0,"binance_public_dynamic":0,"partial":True}
                            for source,collector,key in (("YAHOO",lambda:yahoo_once(folder,"MONDAY",stamp),"yahoo"),
                                                         ("BINANCE_PUBLIC_DYNAMIC",lambda:public_dynamic(folder,stamp),"binance_public_dynamic")):
                                try: slot_success[stamp][key]=collector()
                                except Exception as e:
                                    slot_success[stamp][source.lower()+"_error"]=type(e).__name__+": "+str(e)[:180]
                                    append(folder/"errors.jsonl",{"origin":"FALLBACK","at":now(),"scheduled_at":stamp,"source":source,"error_type":type(e).__name__,"message":str(e)[:240]})
                                    if getattr(e,"status",None)==429 or getattr(e,"code",None) in (429,42900):
                                        retry=getattr(e,"retry",None)
                                        try: wait=max(900,int(retry or 0))
                                        except (ValueError,TypeError): wait=900
                                        cooldown=max(cooldown,time.time()+wait)
                                        atomic(folder/"backoff.json",{"not_before_epoch":cooldown,"updated_at":now(),"reason":"429; minimum 900 seconds"})
                            slot_success[stamp]["partial"]=slot_success[stamp]["yahoo"]<3 or slot_success[stamp]["binance_public_dynamic"]<6
                        else: capture_local(MONDAY,"MONDAY",stamp)
                    except Exception as e:
                        retry=getattr(e,"retry",None)
                        try: wait=max(900,int(retry or 0)) if getattr(e,"status",None)==429 or getattr(e,"code",None) in (429,42900) else max(1,min(300,int(retry))) if retry else 15
                        except (ValueError,TypeError): wait=900 if getattr(e,"status",None)==429 or getattr(e,"code",None) in (429,42900) else 15
                        append(folder/"errors.jsonl",{"origin":"FALLBACK","at":now(),"scheduled_at":stamp,"error_type":type(e).__name__,"message":str(e)[:240],"retry_in_seconds":wait})
                        if getattr(e,"status",None)==429 or getattr(e,"code",None) in (429,42900):
                            cooldown=max(cooldown,time.time()+wait); atomic(folder/"backoff.json",{"not_before_epoch":cooldown,"updated_at":now(),"reason":"429; minimum 900 seconds"})
                next_capture= max(next_capture, scheduled+60)
                # Drop elapsed minute slots and record them, never replay a stale observation under a later slot.
                while next_capture<=time.time():
                    record_gap(folder,next_capture,next_capture,"capture_overran_slot; no catch-up")
                    next_capture+=60
            if not public and t>=next_health:
                health=primary_health(); append(folder/"opening-health.jsonl",health)
                bad=not health["collector_pid_alive"] or not health["watchdog_alive"] or health["latest_complete_slot"] is None or health["seconds_since_last_successful_observation"] is None or health["seconds_since_last_successful_observation"]>600 or health["underlying_watch_age_seconds"] is None or health["underlying_watch_age_seconds"]>2100
                state="FAILURE" if bad else "HEALTHY"
                if state!=previous: print(json.dumps({"at":now(),"opening_health_state":state,"health":health}),flush=True); previous=state
                next_health=time.time()+10
            time.sleep(1)
        else: time.sleep(min(10,max(1,START-t)))
    expected=[slot_text(START+i*60) for i in range(25)]
    incomplete=[stamp for stamp in expected if stamp not in slot_success or slot_success[stamp].get("yahoo",0)<3 or slot_success[stamp].get("binance_public_dynamic",0)<6]
    atomic(folder/"finished.json",{"origin":"FALLBACK","finished_at":now(),"window_end":datetime.fromtimestamp(END,timezone.utc).isoformat(),"public_slots":slot_success,"expected_slot_count":len(expected),"incomplete_slots":incomplete,"alert":"one or more scheduled public slots missing or partial" if incomplete else None})
    if public and incomplete: raise SystemExit(1)

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("command",choices=("once","start","loop","status","public-loop","public-once","public-close")); args=parser.parse_args()
    if args.command=="once":
        PREFLIGHT.mkdir(parents=True,exist_ok=True); result=capture_local(PREFLIGHT,"PREFLIGHT"); atomic(PREFLIGHT/"summary.json",result); print(json.dumps(result,sort_keys=True)); return
    if args.command=="public-once":
        folder=Path(os.environ.get("MONDAY_FALLBACK_OUTPUT_DIR",str(ROOT/"data/monday_open_fallback/public-preflight")))/"PREFLIGHT"
        folder.mkdir(parents=True,exist_ok=True)
        try: count=yahoo_once(folder,"PREFLIGHT")
        except Exception as e:
            count=0; append(folder/"errors.jsonl",{"origin":"FALLBACK","mode":"PREFLIGHT","source":"YAHOO","at":now(),"error_type":type(e).__name__,"message":str(e)[:200]})
        try: dynamic_count=public_dynamic(folder,now(),"PREFLIGHT")
        except Exception as e:
            dynamic_count=0; append(folder/"errors.jsonl",{"origin":"FALLBACK","mode":"PREFLIGHT","source":"BINANCE_PUBLIC_DYNAMIC","at":now(),"error_type":type(e).__name__,"message":str(e)[:200]})
        result={"origin":"FALLBACK","mode":"PREFLIGHT","yahoo_tickers_responded":count,"yahoo_expected":3,"public_dynamic_contracts_responded":dynamic_count,"public_dynamic_expected":6,"status":"INTRADAY_SUPPORTING_ONLY"}
        atomic(folder/"summary.json",result)
        print(json.dumps({**result,"output_dir":str(folder)}))
        if count<3 or dynamic_count<6: raise SystemExit(1)
        return
    if args.command=="public-close":
        if time.time()<datetime(2026,10,5,20,5,tzinfo=timezone.utc).timestamp(): raise SystemExit("public-close is available after 2026-10-05T20:05:00Z")
        folder=Path(os.environ.get("MONDAY_FALLBACK_OUTPUT_DIR",str(ROOT/"data/monday_open_fallback/public")))/"CLOSE"
        found=yahoo_close(folder); result={"origin":"FALLBACK","mode":"MONDAY_CLOSE_SUPPORTING_ONLY","dated_rows_found":found,"expected":3,"output_dir":str(folder)}
        atomic(folder/"summary.json",result); print(json.dumps(result))
        if found<1: raise SystemExit(1)
        return
    if args.command in ("loop","public-loop"): loop(args.command=="public-loop"); return
    if args.command=="start":
        MONDAY.mkdir(parents=True,exist_ok=True)
        pidfile=MONDAY/"pid.json"; saved=read(pidfile); pid=saved.get("pid")
        if process_alive(pid,"monday_open_fallback.py"): print(json.dumps({"already_running":True,"pid":pid})); return
        with (MONDAY/"process.log").open("a") as log:
            child=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),"loop"],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        caffeinate_pid=None
        if sys.platform=="darwin":
            with (MONDAY/"caffeinate.log").open("a") as log:
                keeper=subprocess.Popen(["/usr/bin/caffeinate","-s","-w",str(child.pid)],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            caffeinate_pid=keeper.pid; (MONDAY/"caffeinate.pid").write_text(str(keeper.pid)+"\n")
        print(json.dumps({"fallback_pid":child.pid,"caffeinate_pid":caffeinate_pid,"scheduled_window_utc":"2026-10-05T13:20:00Z/2026-10-05T13:45:00Z"})); return
    health=primary_health(); fallback=last_jsonl(MONDAY/"opening-health.jsonl")
    fallback_pid=read(MONDAY/"pid.json").get("pid")
    fallback_running=process_alive(fallback_pid,"monday_open_fallback.py")
    local_preflight=read(PREFLIGHT/"summary.json").get("complete") is True
    public_summary=read(Path(os.environ.get("MONDAY_FALLBACK_OUTPUT_DIR",str(ROOT/"data/monday_open_fallback/public-preflight")))/"PREFLIGHT"/"summary.json")
    public_preflight=public_summary.get("yahoo_tickers_responded",0)>=3 and public_summary.get("public_dynamic_contracts_responded",0)>=6
    preflight_ready=local_preflight
    ready=bool(preflight_ready and fallback_running and health["collector_pid_alive"] and health["watchdog_alive"] and health["latest_complete_slot"] is not None and health["seconds_since_last_successful_observation"] is not None and health["seconds_since_last_successful_observation"]<=600 and health["underlying_watch_age_seconds"] is not None and health["underlying_watch_age_seconds"]<=2100)
    points=["Mac mini power/network/filesystem for PRIMARY and local fallback","Binance Web3 API availability and credentials for local capture","single local runtime/process for fallback","Yahoo Finance availability for credential-free public path","GitHub Actions schedule/runner availability if public-loop is used"]
    print(json.dumps({"MONDAY_OPEN_READY":"YES" if ready else "NO","preflight_ready_local":local_preflight,"public_preflight_ready_in_this_runtime":public_preflight,"local_fallback_process_alive":fallback_running,"primary_health":health,"fallback_health":fallback,"single_points_of_failure":points},indent=2,sort_keys=True))
    if not ready: raise SystemExit(1)
if __name__=="__main__": main()
