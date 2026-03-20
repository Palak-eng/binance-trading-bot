from __future__ import annotations

from decimal import Decimal, InvalidOperation

from .exceptions import ValidationError

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def normalize_symbol(symbol: str) -> str:
    if not symbol or not symbol.strip():
        raise ValidationError("Symbol is required.")
    symbol = symbol.strip().upper()
    if not symbol.isalnum():
        raise ValidationError("Symbol must be alphanumeric, for example: BTCUSDT.")
    return symbol


def normalize_side(side: str) -> str:
    value = (side or "").strip().upper()
    if value not in VALID_SIDES:
        raise ValidationError("Invalid side. Use BUY or SELL.")
    return value


def normalize_order_type(order_type: str) -> str:
    value = (order_type or "").strip().upper()
    if value not in VALID_ORDER_TYPES:
        raise ValidationError("Invalid order type. Use MARKET or LIMIT.")
    return value


def _to_positive_decimal(value: str | float | int, field_name: str) -> str:
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"{field_name.capitalize()} must be a valid number.") from exc

    if dec <= 0:
        raise ValidationError(f"{field_name.capitalize()} must be greater than 0.")

    normalized = format(dec.normalize(), "f")
    if "." in normalized:
        normalized = normalized.rstrip("0").rstrip(".")
    return normalized


def normalize_quantity(quantity: str | float | int) -> str:
    return _to_positive_decimal(quantity, "quantity")


def normalize_price(price: str | float | int | None, order_type: str) -> str | None:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("LIMIT order requires --price.")
        return _to_positive_decimal(price, "price")

    if price is not None:
        return _to_positive_decimal(price, "price")

    return None


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float | int,
    price: str | float | int | None = None,
) -> dict[str, str]:
    normalized_type = normalize_order_type(order_type)

    payload = {
        "symbol": normalize_symbol(symbol),
        "side": normalize_side(side),
        "type": normalized_type,
        "quantity": normalize_quantity(quantity),
    }

    normalized_price = normalize_price(price, normalized_type)
    if normalized_price is not None:
        payload["price"] = normalized_price

    return payload