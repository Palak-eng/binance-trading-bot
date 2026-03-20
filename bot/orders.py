from __future__ import annotations

from typing import Any

from .client import BinanceFuturesClient


def build_order_payload(validated_input: dict[str, str]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "symbol": validated_input["symbol"],
        "side": validated_input["side"],
        "type": validated_input["type"],
        "quantity": validated_input["quantity"],
        "newOrderRespType": "RESULT",
    }

    if validated_input["type"] == "LIMIT":
        payload["timeInForce"] = "GTC"
        payload["price"] = validated_input["price"]

    return payload


def place_order(
    client: BinanceFuturesClient,
    validated_input: dict[str, str],
    test: bool = False,
) -> dict[str, Any]:
    payload = build_order_payload(validated_input)

    if test:
        client.create_test_order(payload)
        return {
            "message": "Test order successful (not executed).",
            "payload": payload,
        }

    response = client.create_order(payload)

    # LIMIT orders may return NEW and avgPrice can be missing/0.
    # Fetch once more for cleaner response.
    if response.get("orderId") and validated_input["type"] == "LIMIT":
        try:
            latest = client.get_order(validated_input["symbol"], int(response["orderId"]))
            response.update(latest)
        except Exception:
            # Keep original response if follow-up fetch fails.
            pass

    return response