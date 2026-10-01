#!/usr/bin/env python3
"""Read-only, market-level Venus scenario server. Python 3.9 standard library only."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
from urllib.parse import urlparse, parse_qs

getcontext().prec = 36
API_URL = "https://api.venus.io/markets?chainId=56&limit=100"
CHAIN = "56"
NVDAB = "0x02fca66c1d1afb4e2a7884261eb00f63598a7436"
USDT = "0x55d398326f99059ff775485246999027b3197955"
ZERO = Decimal("0")
MAX_INPUT = Decimal("1000000000000000")
MIN_INPUT = Decimal("0.000000000000000001")


class ScenarioError(Exception):
    def __init__(self, field, message):
        self.field, self.message = field, message


def decimal_input(value, field):
    try:
        number = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ScenarioError(field, "Enter a valid number.")
    if not number.is_finite() or number <= ZERO:
        raise ScenarioError(field, "Enter an amount greater than zero.")
    if number < MIN_INPUT or number > MAX_INPUT:
        raise ScenarioError(field, "Use an amount from 0.000000000000000001 to 1,000,000,000,000,000.")
    return number


def fetch_markets():
    request = Request(API_URL, headers={"User-Agent": "Dyplux-Venus-Scenario/0.1 (read-only)"})
    with urlopen(request, timeout=12) as response:
        if response.status != 200:
            raise RuntimeError("Venus API returned HTTP %s." % response.status)
        return json.loads(response.read().decode("utf-8"))


def d(value):
    if value in (None, ""):
        return None
    try:
        result = Decimal(str(value))
        return result if result.is_finite() else None
    except InvalidOperation:
        return None


def market_rows(data):
    rows = data.get("result", []) if isinstance(data, dict) else []
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise RuntimeError("Venus returned an invalid market list.")
    return rows


def unique_market(rows, address, symbol):
    matches = [row for row in rows if row.get("chainId") == CHAIN
               and row.get("underlyingSymbol") == symbol
               and (row.get("underlyingAddress") or "").lower() == address]
    if len(matches) != 1:
        raise RuntimeError("Venus did not return exactly one verified %s market for BNB Chain." % symbol)
    return matches[0]


def build_scenario(units, cash, data, retrieved_at):
    rows = market_rows(data)
    stock = unique_market(rows, NVDAB, "NVDAB")
    pool = stock.get("poolComptrollerAddress")
    if not pool:
        raise RuntimeError("Venus NVDAB pool identity is unavailable.")
    usdt_matches = [row for row in rows if row.get("chainId") == CHAIN
                    and (row.get("poolComptrollerAddress") or "").lower() == pool.lower()
                    and row.get("underlyingSymbol") == "USDT"
                    and (row.get("underlyingAddress") or "").lower() == USDT]
    if len(usdt_matches) != 1:
        raise RuntimeError("Venus did not return exactly one verified USDT market in the NVDAB pool.")
    usdt = usdt_matches[0]
    if stock.get("isListed") is not True or stock.get("canBeCollateral") is not True:
        raise RuntimeError("NVDAB is not currently listed and enabled as collateral.")
    price_m, decimals = d(stock.get("underlyingPriceMantissa")), d(stock.get("underlyingDecimal"))
    cf, lt = d(stock.get("collateralFactorMantissa")), d(stock.get("liquidationThresholdMantissa"))
    if stock.get("isPriceInvalid") is True or price_m is None or price_m <= 0:
        raise RuntimeError("Venus NVDAB price is invalid or unavailable.")
    if decimals is None or decimals < 0 or decimals > 36 or decimals != decimals.to_integral_value():
        raise RuntimeError("Venus returned invalid NVDAB decimals.")
    scale = Decimal(10) ** 18
    if cf is None or lt is None or cf <= 0 or lt <= 0 or cf > scale or lt > scale:
        raise RuntimeError("Venus collateral or liquidation factor is unavailable.")
    if usdt.get("isListed") is not True or usdt.get("isBorrowable") is not True:
        raise RuntimeError("Venus USDT borrowing is currently unavailable.")

    # Venus documented mantissa scale: 1e(36 - underlying decimals).
    price = price_m / (Decimal(10) ** (36 - int(decimals)))
    usdt_price_m, usdt_decimals = d(usdt.get("underlyingPriceMantissa")), d(usdt.get("underlyingDecimal"))
    if usdt.get("isPriceInvalid") is True or usdt_price_m is None or usdt_price_m <= 0:
        raise RuntimeError("Venus USDT oracle price is invalid or unavailable.")
    if usdt_decimals is None or usdt_decimals < 0 or usdt_decimals > 36 or usdt_decimals != usdt_decimals.to_integral_value():
        raise RuntimeError("Venus returned invalid USDT decimals.")
    usdt_price = usdt_price_m / (Decimal(10) ** (36 - int(usdt_decimals)))
    borrow_rate = d(usdt.get("borrowApyDecimal"))
    cash_raw = d(usdt.get("cashMantissa"))
    if price <= 0 or usdt_price <= 0 or borrow_rate is None or borrow_rate < 0 or cash_raw is None or cash_raw < 0:
        raise RuntimeError("Venus USDT rate, oracle price or pool cash is unavailable.")
    pool_cash = cash_raw / (Decimal(10) ** int(usdt_decimals))
    collateral_value_usd = units * price
    collateral_value_usdt = collateral_value_usd / usdt_price
    capacity = collateral_value_usdt * cf / scale
    threshold = lt / scale
    liquidation_weighted_usdt = collateral_value_usd * threshold / usdt_price
    health = liquidation_weighted_usdt / cash
    drop = (Decimal(1) - (cash * usdt_price / (collateral_value_usd * threshold))) * 100 if collateral_value_usd * threshold > cash * usdt_price else None
    return {
        "retrieved_at": retrieved_at, "source_url": API_URL, "chain_id": 56,
        "scenario_only": True,
        "assumptions": ["No wallet debt or other collateral", "No E-Mode", "No accrued interest or execution costs", "Market-level snapshot, not a personal safety assessment"],
        "input": {"units": str(units), "cash_usdt": str(cash)},
        "market": {"nvdab_price_usd": str(price), "usdt_oracle_price_usd": str(usdt_price), "collateral_factor": str(cf / scale), "liquidation_threshold": str(threshold), "borrow_apy": str(borrow_rate), "pool_cash_usdt": str(pool_cash), "nvdab_market": stock.get("address"), "usdt_market": usdt.get("address"), "pool_comptroller": pool, "data_status": "indexed Venus API snapshot, may lag the chain"},
        "borrow": {"nominal_capacity_usdt": str(capacity), "target_feasible_by_collateral": cash <= capacity,
                   "target_feasible_by_pool_liquidity": cash <= pool_cash,
                   "health_factor": str(health), "price_drop_to_hf_1_percent": str(drop) if drop is not None else None,
                   "interest_30d_usdt": str(cash * borrow_rate * Decimal(30) / Decimal(365)),
                   "interest_90d_usdt": str(cash * borrow_rate * Decimal(90) / Decimal(365)),
                   "interest_note": "Simple interest at the current variable APY, held flat for illustration."},
        "sale": {"status": "unquoted", "message": "No Binance Web3 sell quote is connected. Proceeds are unknown."}
    }


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            try:
                with open("app/index.html", "rb") as page:
                    body = page.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except OSError:
                self.send_error(500)
            return
        if parsed.path != "/api/scenario":
            self.send_error(404)
            return
        query = parse_qs(parsed.query)
        try:
            units = decimal_input(query.get("units", [""])[0], "units")
            cash = decimal_input(query.get("cash", [""])[0], "cash")
            data = fetch_markets()
            result = build_scenario(units, cash, data, datetime.now(timezone.utc).isoformat(timespec="seconds"))
            self.send_json(200, result)
        except ScenarioError as exc:
            self.send_json(400, {"error": {"field": exc.field, "message": exc.message}})
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
            self.send_json(502, {"error": {"field": "service", "message": "Live Venus data is unavailable. No scenario was calculated.", "detail": str(exc)[:180]}})

    def log_message(self, fmt, *args):
        # Keep access logs free of entered query amounts.
        if self.path.startswith("/api/"):
            print("%s - scenario request" % self.address_string())
        else:
            super().log_message(fmt, *args)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Read-only scenario at http://127.0.0.1:8000")
    server.serve_forever()
