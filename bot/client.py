from __future__ import annotations

import hashlib
import hmac
import logging
import os
from typing import Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from .exceptions import BinanceAPIError, NetworkError

load_dotenv()

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """Minimal Binance Futures Testnet REST client using signed requests."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        base_url: str | None = None,
        timeout: int = 15,
    ) -> None:
        self.api_key = api_key or os.getenv("BINANCE_API_KEY", "")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET", "")
        self.base_url = (
            base_url
            or os.getenv("BINANCE_BASE_URL")
            or "https://testnet.binancefuture.com"
        ).rstrip("/")
        self.timeout = timeout

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Missing Binance API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET."
            )

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def get_server_time(self) -> int:
        """Fetch Binance server time to avoid local clock drift issues."""
        try:
            response = self.session.get(
                f"{self.base_url}/fapi/v1/time",
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()["serverTime"]
        except requests.exceptions.RequestException as exc:
            logger.exception("Failed to fetch server time")
            raise NetworkError(f"Failed to get server time: {exc}") from exc

    def _sign_params(self, params: dict[str, Any]) -> str:
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"{query_string}&signature={signature}"

    def _request(
        self,
        method: str,
        path: str,
        signed: bool = False,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        params = params or {}
        url = f"{self.base_url}{path}"

        if signed:
            params["timestamp"] = self.get_server_time()
            params.setdefault("recvWindow", 10000)
            payload = self._sign_params(params)
        else:
            payload = urlencode(params, doseq=True)

        logger.info(
            "API request | method=%s | url=%s | payload=%s",
            method,
            url,
            payload,
        )

        try:
            upper_method = method.upper()
            response = self.session.request(
                method=method,
                url=url,
                params=payload if signed and upper_method == "GET" else (None if signed else params),
                data=payload if signed and upper_method in {"POST", "PUT", "DELETE"} else None,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as exc:
            logger.exception("Network error while calling Binance")
            raise NetworkError(f"Network error: {exc}") from exc

        text = response.text
        logger.info(
            "API response | status_code=%s | body=%s",
            response.status_code,
            text,
        )

        try:
            data = response.json()
        except ValueError as exc:
            logger.exception("Failed to parse JSON response")
            raise BinanceAPIError(f"Non-JSON response: {text}") from exc

        if response.status_code >= 400:
            code = data.get("code", "UNKNOWN")
            msg = data.get("msg", "Unknown Binance API error")
            raise BinanceAPIError(f"Binance API error {code}: {msg}")

        return data

    def ping(self) -> dict[str, Any]:
        return self._request("GET", "/fapi/v1/ping")

    def create_order(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/fapi/v1/order", signed=True, params=params)

    def create_test_order(self, params: dict[str, Any]) -> dict[str, Any]:
        """Submit a Binance test order that validates request without execution."""
        return self._request("POST", "/fapi/v1/order/test", signed=True, params=params)

    def get_order(self, symbol: str, order_id: int) -> dict[str, Any]:
        return self._request(
            "GET",
            "/fapi/v1/order",
            signed=True,
            params={"symbol": symbol, "orderId": order_id},
        )