"""One live, read-only stock-token action review. No wallet signing or broadcast."""

import secrets
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from app.rwa_policy import evaluate
from app.server import USDT
from app.public_stock_info import fetch as public_stock_info
from scripts.audit_onchain_multiplier import SELECTORS, call, rpc_batch
from scripts.rwa_research import Api, PRICE, QUOTE, TOKENS, UNDERLYING_MARKET, normalize

EXPERIMENT = "H-RWA-SAFETY/PRODUCT"
PROVIDERS = {"bstock": "NVDAB", "ondo": "NVDAon"}
ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\Z")


def amount(value, field, low, high):
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("%s must be a number" % field)
    if not number.is_finite() or number < low or number > high:
        raise ValueError("%s must be between %s and %s" % (field, low, high))
    return number


def validate(request):
    if not isinstance(request, dict):
        raise ValueError("Expected one action request")
    allowed = {"provider", "notional_usdt", "max_notional_usdt", "max_price_impact_percent"}
    if set(request) - allowed:
        raise ValueError("Only action and mandate fields are accepted; never send wallet secrets")
    provider = request.get("provider")
    if provider not in PROVIDERS:
        raise ValueError("Choose NVDAB or NVDAon")
    notional = amount(request.get("notional_usdt"), "Amount", Decimal("10"), Decimal("1000"))
    limit = amount(request.get("max_notional_usdt"), "Mandate limit", Decimal("1"), Decimal("1000"))
    impact = amount(request.get("max_price_impact_percent"), "Impact limit", Decimal("0.001"), Decimal("5"))
    if notional.as_tuple().exponent < -18:
        raise ValueError("Amount has more than 18 decimal places")
    return provider, notional, limit, impact


def data_row(payload, contract):
    rows = payload.get("data") if isinstance(payload.get("data"), list) else []
    return next((row for row in rows if isinstance(row, dict) and
                 str(row.get("tokenContractAddress", "")).lower() == contract), None)


def route_matches_action(route, source, destination, raw_amount):
    if not isinstance(route, dict):
        return False
    from_token = route.get("fromToken") or {}
    to_token = route.get("toToken") or {}
    try:
        output = Decimal(str(route.get("toTokenAmount")))
    except (InvalidOperation, TypeError, ValueError):
        return False
    return (str(route.get("binanceChainId")) == "56" and
            isinstance(from_token, dict) and isinstance(to_token, dict) and
            str(from_token.get("tokenContractAddress", "")).lower() == source.lower() and
            str(to_token.get("tokenContractAddress", "")).lower() == destination.lower() and
            str(route.get("fromTokenAmount")) == str(raw_amount) and
            output.is_finite() and output > 0)


def multiplier(contract, rpc=rpc_batch):
    head, _, _, head_hash = rpc([call("eth_blockNumber", [], 1)], "latest", EXPERIMENT)
    block = head[0]["result"]
    header, _, _, header_hash = rpc([call("eth_getBlockByNumber", [block, False], 2)], block, EXPERIMENT)
    timestamp = int(header[0]["result"]["timestamp"], 16)
    calls = [call("eth_call", [{"to": contract, "data": selector}, block], index)
             for index, selector in enumerate(SELECTORS.values(), 10)]
    replies, _, _, value_hash = rpc(calls, block, EXPERIMENT)
    values = {int(row["id"]): int(row["result"], 16) for row in replies}
    if set(values) != {10, 11, 12}:
        raise ValueError("Incomplete fixed-block multiplier state")
    return {
        "onchain_ui_multiplier": str(Decimal(values[10]) / Decimal(10**18)),
        "onchain_new_ui_multiplier": str(Decimal(values[11]) / Decimal(10**18)),
        "onchain_multiplier_effective_at": values[12],
        "onchain_multiplier_block": int(block, 16),
        "onchain_multiplier_block_timestamp": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
        "rpc_response_sha256": [head_hash, header_hash, value_hash],
    }


def review(request, api=None, rpc=rpc_batch, stock_info=public_stock_info,
           quote_wallet=None, return_route_context=False):
    provider, notional, limit, impact_limit = validate(request)
    if quote_wallet is not None and not ADDRESS.fullmatch(quote_wallet):
        raise ValueError("Invalid public quote wallet address")
    if return_route_context and quote_wallet is None:
        raise ValueError("An exact wallet is required for route context")
    api = api or Api()
    errors = []
    context = {"task": "one_NVDA_buy_review", "provider": provider, "origin": "LIVE"}
    catalog, captured_at, catalog_hash = api.get(
        TOKENS, [("binanceChainId", "56")], EXPERIMENT,
        "BSC RWA catalog for exact security and representation", context)
    candidates = [normalize(row) for row in catalog["data"]]
    matches = [row for row in candidates if row and row["provider"] == provider and
               row["ticker"] == "NVDA" and row["token_symbol"] == PROVIDERS[provider] and
               row["asset_type"] == 1]
    if len(matches) != 1:
        raise RuntimeError("Live catalog could not identify exactly one requested NVDA representation")
    target = matches[0]
    contract = target["contract"]
    evidence = {
        "chain_id": "56", "ticker": "NVDA", "provider": provider, "contract": contract,
        "issuer_verified": False, "eligibility_status": "UNKNOWN",
        "token_to_share_ratio": target["token_to_share_ratio"],
        "market_status": target["market_status"], "market_reason": target["market_reason"],
        "reference_price_updated_at": None, "reference_age_seconds": None,
        "reference_age_status": "UNKNOWN", "quote_available": None,
        "quote_identity_match": None,
        "simulation_passed": False, "source_response_sha256": catalog_hash,
    }
    sources = {"catalog": {"observed_at": captured_at, "sha256": catalog_hash},
               "price": None, "underlying_market": None, "stock_info": None,
               "quote": None, "rpc": None}
    view = {"canonical_security": "NVDA", "representation": target["token_symbol"],
            "provider": provider, "contract": contract, "market_status": target["market_status"],
            "market_open_state": None, "token_price_usd": None, "token_price_updated_at": None,
            "token_price_age_ms": None, "reported_reference_price_usd": None,
            "stock_feed_price_usd": None, "stock_feed_price_asof": None,
            "reference_price_updated_at": None, "reference_age_status": "UNKNOWN",
            "token_to_share_ratio": target["token_to_share_ratio"],
            "multiplier_integrity": "UNKNOWN" if provider == "bstock" else "NOT_APPLICABLE",
            "eligibility": "UNKNOWN", "route": "UNKNOWN", "execution_mode": None,
            "price_impact_percent": None, "simulation": "NOT_RUN", "quote_vendor": None}
    try:
        payload, at, digest = api.get(
            PRICE, [("binanceChainId", "56"), ("tokenContractAddresses", contract)],
            EXPERIMENT, "live token price with its own timestamp", context)
        row = data_row(payload, contract)
        if row is None:
            raise ValueError("Price row for exact contract missing")
        stamp = row.get("tokenPriceUpdatedAt")
        observed = datetime.fromisoformat(at.replace("Z", "+00:00"))
        age = int(observed.timestamp() * 1000) - stamp if isinstance(stamp, int) else None
        evidence.update({"token_price_age_ms": age,
                         "token_price_age_calculation": "observed_at_minus_tokenPriceUpdatedAt",
                         "token_price_usd": row.get("tokenPrice"),
                         "reported_reference_price_usd": row.get("referencePrice")})
        view.update({"token_price_usd": row.get("tokenPrice"),
                     "reported_reference_price_usd": row.get("referencePrice"),
                     "token_price_updated_at": datetime.fromtimestamp(stamp / 1000, timezone.utc).isoformat() if isinstance(stamp, int) else None,
                     "token_price_age_ms": age})
        sources["price"] = {"observed_at": at, "sha256": digest}
    except Exception as exc:
        errors.append({"source": "price", "type": type(exc).__name__})
    try:
        payload, at, digest = api.get(
            UNDERLYING_MARKET, [("binanceChainId", "56"), ("tokenContractAddress", contract)],
            EXPERIMENT, "market state and independent reference timestamp availability", context)
        state = payload["data"].get("statusInfo") or {}
        market = payload["data"].get("marketData") or {}
        evidence.update({"market_status": state.get("marketStatus"),
                         "market_reason": state.get("reasonCode"),
                         "market_open_state": state.get("openState"),
                         "reported_reference_price_usd": market.get("referencePrice") or evidence.get("reported_reference_price_usd")})
        view.update({"market_status": state.get("marketStatus"),
                     "market_open_state": state.get("openState"),
                     "reported_reference_price_usd": market.get("referencePrice") or view["reported_reference_price_usd"]})
        sources["underlying_market"] = {"observed_at": at, "sha256": digest}
    except Exception as exc:
        errors.append({"source": "underlying_market", "type": type(exc).__name__})
        evidence["market_status"] = None
        view["market_status"] = None
    if provider == "ondo":
        try:
            stock, at, digest = stock_info(contract)
            if stock.get("ticker") != "NVDA" or stock.get("symbol") != "NVDAon":
                raise ValueError("Public stock-info identity mismatch")
            info = stock.get("stockInfo") if isinstance(stock.get("stockInfo"), dict) else {}
            view["stock_feed_price_usd"] = info.get("price")
            evidence["stock_feed_price_usd"] = info.get("price")
            evidence["stock_feed_price_asof"] = None
            sources["stock_info"] = {"observed_at": at, "sha256": digest,
                                     "stock_price_asof": None}
        except Exception as exc:
            errors.append({"source": "public_stock_info", "type": type(exc).__name__})
    if provider == "bstock":
        try:
            state = multiplier(contract, rpc)
            evidence.update({k: state[k] for k in (
                "onchain_ui_multiplier", "onchain_multiplier_effective_at",
                "onchain_multiplier_block", "onchain_multiplier_block_timestamp")})
            evidence["onchain_new_ui_multiplier"] = state["onchain_new_ui_multiplier"]
            view["multiplier_integrity"] = (
                "MATCHED_FIXED_BLOCK" if Decimal(state["onchain_ui_multiplier"]) == Decimal(str(target["token_to_share_ratio"])) and
                Decimal(state["onchain_new_ui_multiplier"]) == Decimal(state["onchain_ui_multiplier"]) and
                state["onchain_multiplier_effective_at"] == 0 else "REVIEW_REQUIRED")
            sources["rpc"] = {"block": state["onchain_multiplier_block"],
                              "block_timestamp": state["onchain_multiplier_block_timestamp"],
                              "sha256": state["rpc_response_sha256"]}
        except Exception as exc:
            errors.append({"source": "rpc_multiplier", "type": type(exc).__name__})
    route = None
    wallet = quote_wallet or "0x" + secrets.token_hex(20)
    try:
        raw_amount = int(notional * Decimal(10**18))
        payload, at, digest = api.get(
            QUOTE, [("binanceChainId", "56"), ("fromTokenAddress", USDT),
                    ("toTokenAddress", contract), ("amount", str(raw_amount)),
                    ("userWalletAddress", wallet)],
            EXPERIMENT, "one size-specific read-only USDT buy route", context, allow_error=True)
        routes = payload.get("data") if isinstance(payload.get("data"), list) else []
        matching = [r for r in routes if route_matches_action(r, USDT, contract, raw_amount)]
        route = next((r for r in matching if r.get("isBest") is True), matching[0] if matching else None)
        evidence["quote_available"] = bool(route)
        evidence["quote_identity_match"] = True if route else (False if routes else None)
        if route:
            evidence["price_impact_percent"] = route.get("priceImpactPercent")
            evidence["quote_execution_mode"] = route.get("executionMode")
            evidence["quote_vendor"] = route.get("vendorName")
            evidence["quote_observed_at"] = at
            view.update({"route": "QUOTED", "execution_mode": route.get("executionMode"),
                         "quote_vendor": route.get("vendorName"),
                         "price_impact_percent": route.get("priceImpactPercent")})
        else:
            view["route"] = "MISMATCH" if routes else "NO_ROUTE"
            if routes:
                errors.append({"source": "quote_identity", "type": "RouteIntentMismatch"})
        sources["quote"] = {"observed_at": at, "sha256": digest,
                            "business_code": payload.get("code"), "route_count": len(routes)}
    except Exception as exc:
        errors.append({"source": "quote", "type": type(exc).__name__})
    intent = {"chain_id": "56", "ticker": "NVDA", "provider": provider,
              "contract": contract, "notional_usd": str(notional)}
    mandate = {"max_notional_usd": str(limit), "max_price_impact_percent": str(impact_limit),
               "max_token_price_age_ms": 60_000, "require_independent_reference": True,
               "max_reference_age_seconds": 300, "max_eligibility_age_seconds": 3600,
               "require_onchain_multiplier": provider == "bstock",
               "max_onchain_multiplier_age_seconds": 120}
    evidence["source_response_sha256"] = {key: source.get("sha256") for key, source in sources.items()
                                          if isinstance(source, dict)}
    evidence["source_observed_at"] = {key: source.get("observed_at") for key, source in sources.items()
                                     if isinstance(source, dict) and source.get("observed_at")}
    receipt = evaluate(intent, evidence, mandate, now=datetime.now(timezone.utc))
    result = {"origin": "LIVE_READ_ONLY", "action": "BUY_NVDA_WITH_USDT",
            "decision": receipt["decision"], "reason_codes": receipt["reason_codes"],
            "view": view, "mandate": mandate, "sources": sources, "errors": errors,
            "receipt": receipt,
            "limits": "No eligibility decision, holder wallet, funded simulation, signature, transaction, fill, or independent stock-reference timestamp."}
    if not return_route_context:
        return result
    return result, {"wallet": wallet, "route": route, "provider": provider,
                    "ticker": "NVDA", "symbol": target["token_symbol"],
                    "contract": contract, "raw_amount": str(raw_amount),
                    "quote_observed_at": (sources["quote"] or {}).get("observed_at"),
                    "quote_sha256": (sources["quote"] or {}).get("sha256"),
                    "catalog_observed_at": sources["catalog"]["observed_at"],
                    "catalog_sha256": sources["catalog"]["sha256"]}
