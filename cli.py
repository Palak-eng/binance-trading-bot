from __future__ import annotations
from colorama import Fore, Style, init
import argparse
import logging
import sys
from pprint import pformat

from bot.client import BinanceFuturesClient
from bot.exceptions import BinanceAPIError, NetworkError, ValidationError
from bot.logging_config import setup_logging
from bot.orders import build_order_payload, place_order
from bot.validators import validate_order_input
init(autoreset=True)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet orders from the CLI"
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price", help="Required for LIMIT orders")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Use Binance test endpoint (order will NOT be executed)",
    )
    return parser.parse_args()


def print_order_summary(validated_input: dict[str, str], test: bool) -> None:
    print(Fore.CYAN + "\n=== ORDER REQUEST SUMMARY ===")
    print(Fore.YELLOW + f"Symbol      : {validated_input['symbol']}")
    print(Fore.YELLOW + f"Side        : {validated_input['side']}")
    print(Fore.YELLOW + f"Order Type  : {validated_input['type']}")
    print(Fore.YELLOW + f"Quantity    : {validated_input['quantity']}")
    print(Fore.YELLOW + f"Price       : {validated_input.get('price', 'N/A')}")
    print(Fore.YELLOW + f"Mode        : {'TEST (no execution)' if test else 'LIVE TESTNET'}")


def print_order_response(response: dict) -> None:
    print(Fore.CYAN + "\n=== ORDER RESPONSE ===")

    if "message" in response:
        print(Fore.GREEN + response["message"])
        print(Fore.MAGENTA + "\nPayload:")
        print(pformat(response.get("payload")))
        return

    print(Fore.GREEN + f"Order ID    : {response.get('orderId', 'N/A')}")
    print(Fore.GREEN + f"Status      : {response.get('status', 'N/A')}")
    print(Fore.GREEN + f"Executed Qty: {response.get('executedQty', 'N/A')}")
    print(Fore.GREEN + f"Avg Price   : {response.get('avgPrice', 'N/A')}")
    print(Fore.MAGENTA + "\nFull response:")
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

        print_order_summary(validated_input, args.test)

        client = BinanceFuturesClient()
        logger.info("Validated order payload: %s", build_order_payload(validated_input))

        response = place_order(client, validated_input, test=args.test)
        print_order_response(response)
        print(Fore.BLUE + "\nProcessing order...")
        print(Fore.GREEN + f"\nSUCCESS: Order submitted successfully. Log file: {log_path}")
        return 0

    except ValidationError as exc:
        logger.exception("Validation failed")
        print(Fore.RED + f"\nFAILED: Validation error -> {exc}")
        return 1
    except BinanceAPIError as exc:
        logger.exception("Binance API error")
        print(Fore.RED + f"\nFAILED: Binance API error -> {exc}")

        return 1
    except NetworkError as exc:
        logger.exception("Network failure")
        print(Fore.RED + f"\nFAILED: Network error -> {exc}")
        return 1
    except ValueError as exc:
        logger.exception("Configuration error")
        print(Fore.RED + f"\nFAILED: Configuration error -> {exc}")
        return 1
    except Exception as exc:
        logger.exception("Unexpected error")
        print(Fore.RED + f"\nFAILED: Unexpected error -> {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())