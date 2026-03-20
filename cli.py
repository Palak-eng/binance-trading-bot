from __future__ import annotations

import argparse
import logging
import sys
from pprint import pformat

from bot.client import BinanceFuturesClient
from bot.exceptions import BinanceAPIError, NetworkError, ValidationError
from bot.logging_config import setup_logging
from bot.orders import build_order_payload, place_order
from bot.validators import validate_order_input

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Place Binance Futures Testnet orders from the CLI")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price", help="Required for LIMIT orders")
    return parser.parse_args()


def print_order_summary(validated_input: dict[str, str]) -> None:
    print("\n=== ORDER REQUEST SUMMARY ===")
    print(f"Symbol      : {validated_input['symbol']}")
    print(f"Side        : {validated_input['side']}")
    print(f"Order Type  : {validated_input['type']}")
    print(f"Quantity    : {validated_input['quantity']}")
    print(f"Price       : {validated_input.get('price', 'N/A')}")


def print_order_response(response: dict) -> None:
    print("\n=== ORDER RESPONSE ===")
    print(f"Order ID    : {response.get('orderId', 'N/A')}")
    print(f"Status      : {response.get('status', 'N/A')}")
    print(f"Executed Qty: {response.get('executedQty', 'N/A')}")
    print(f"Avg Price   : {response.get('avgPrice', 'N/A')}")
    print("\nFull response:")
    print(pformat(response))


def main() -> int:
    log_path = setup_logging()
    args = parse_args()

    try:
        validated_input = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print_order_summary(validated_input)

        client = BinanceFuturesClient()
        logger.info("Validated order payload: %s", build_order_payload(validated_input))
        response = place_order(client, validated_input)
        print_order_response(response)
        print(f"\nSUCCESS: Order submitted successfully. Log file: {log_path}")
        return 0

    except ValidationError as exc:
        logger.exception("Validation failed")
        print(f"\nFAILED: Validation error -> {exc}")
        return 1
    except BinanceAPIError as exc:
        logger.exception("Binance API error")
        print(f"\nFAILED: Binance API error -> {exc}")
        return 1
    except NetworkError as exc:
        logger.exception("Network failure")
        print(f"\nFAILED: Network error -> {exc}")
        return 1
    except ValueError as exc:
        logger.exception("Configuration error")
        print(f"\nFAILED: Configuration error -> {exc}")
        return 1
    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"\nFAILED: Unexpected error -> {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
