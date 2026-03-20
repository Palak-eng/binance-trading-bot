class TradingBotError(Exception):
    """Base exception for the trading bot."""


class ValidationError(TradingBotError):
    """Raised when CLI input is invalid."""


class BinanceAPIError(TradingBotError):
    """Raised when Binance returns an API error."""


class NetworkError(TradingBotError):
    """Raised when a network or timeout issue occurs."""
