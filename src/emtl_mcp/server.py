"""EMTL MCP Server - MCP server for East Money trading library."""

from __future__ import annotations

import os
from datetime import datetime
from functools import lru_cache
from typing import Any

from emtl import ClientManager, DillSerializer, EmtlException, LoginFailedError
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("EMTL - East Money Trading Library")


def get_credentials() -> tuple[str, str]:
    """Get credentials from environment variables.

    Credentials are loaded from:
    - EMTL_USERNAME: East Money account username
    - EMTL_PASSWORD: East Money account password

    Returns:
        Tuple of (username, password)

    Raises:
        ValueError: If credentials are not configured
    """
    username = os.environ.get("EMTL_USERNAME")
    password = os.environ.get("EMTL_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Credentials not configured. Please set EMTL_USERNAME and EMTL_PASSWORD "
            "environment variables in your MCP server configuration."
        )

    return username, password


@lru_cache
def get_client_manager() -> ClientManager:
    """Get or create the shared client manager instance."""
    storage_dir = os.environ.get("EMTL_STORAGE_DIR", "./emtl-cache")
    return ClientManager(DillSerializer(storage_dir))


def get_client() -> Any:
    """Get a logged-in EMT client using configured credentials.

    Returns:
        EMT client instance

    Raises:
        ValueError: If credentials are not configured
        LoginFailedError: If login fails
    """
    username, password = get_credentials()
    manager = get_client_manager()
    return manager.get_client(username, password)


def _extract_data(response: dict[str, Any] | None) -> Any:
    """Extract data from EMT API response.

    EMT API returns:
    - {"Status": 0, "Data": [...]}  on success
    - {"Status": -1, "Message": "..."} on error

    Args:
        response: Raw response from EMT API

    Returns:
        The Data field if Status is 0, otherwise the error response
    """
    if response is None:
        return None

    # If response has Status field, check it
    if "Status" in response:
        status = response.get("Status")
        # Status: 0 = success, -1 = error
        if status == 0:
            return response.get("Data")
        elif status == -1:
            return {
                "error": response.get("Message", "Unknown error"),
                "status": -1
            }

    # Return as-is if no Status field
    return response


@mcp.tool
def query_asset_and_position() -> dict[str, Any]:
    """Query account assets and positions.

    Returns:
        Dictionary containing account assets and position information
    """
    try:
        client = get_client()
        result = client.query_asset_and_position()
        data = _extract_data(result)

        # Handle case where Data is a list with single element
        if isinstance(data, list) and len(data) > 0:
            return data[0] if isinstance(data[0], dict) else {}
        return data if isinstance(data, dict) else {}
    except EmtlException as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool
def query_orders() -> list[dict[str, Any]]:
    """Query current pending orders.

    Returns:
        List of current pending orders
    """
    try:
        client = get_client()
        result = client.query_orders()
        data = _extract_data(result)
        return data if isinstance(data, list) else []
    except EmtlException as e:
        return [{"error": str(e)}]
    except ValueError as e:
        return [{"error": str(e)}]


@mcp.tool
def query_trades() -> list[dict[str, Any]]:
    """Query trade records.

    Returns:
        List of trade records
    """
    try:
        client = get_client()
        result = client.query_trades()
        data = _extract_data(result)
        return data if isinstance(data, list) else []
    except EmtlException as e:
        return [{"error": str(e)}]
    except ValueError as e:
        return [{"error": str(e)}]


@mcp.tool
def query_history_orders(
    size: int = 100,
    start_time: str = "",
    end_time: str = "",
) -> list[dict[str, Any]]:
    """Query historical orders.

    Args:
        size: Number of records to query (default: 100)
        start_time: Start time in format "YYYY-MM-DD" (default: 30 days ago)
        end_time: End time in format "YYYY-MM-DD" (default: today)

    Returns:
        List of historical orders
    """
    try:
        client = get_client()

        # Set default dates if not provided
        if not start_time:
            start_time = (datetime.now()).strftime("%Y-%m-%d")
        if not end_time:
            end_time = (datetime.now()).strftime("%Y-%m-%d")

        result = client.query_history_orders(size, start_time, end_time)
        data = _extract_data(result)
        return data if isinstance(data, list) else []
    except EmtlException as e:
        return [{"error": str(e)}]
    except ValueError as e:
        return [{"error": str(e)}]


@mcp.tool
def query_history_trades(
    size: int = 100,
    start_time: str = "",
    end_time: str = "",
) -> list[dict[str, Any]]:
    """Query historical trades.

    Args:
        size: Number of records to query (default: 100)
        start_time: Start time in format "YYYY-MM-DD" (default: 30 days ago)
        end_time: End time in format "YYYY-MM-DD" (default: today)

    Returns:
        List of historical trades
    """
    try:
        client = get_client()

        # Set default dates if not provided
        if not start_time:
            start_time = (datetime.now()).strftime("%Y-%m-%d")
        if not end_time:
            end_time = (datetime.now()).strftime("%Y-%m-%d")

        result = client.query_history_trades(size, start_time, end_time)
        data = _extract_data(result)
        return data if isinstance(data, list) else []
    except EmtlException as e:
        return [{"error": str(e)}]
    except ValueError as e:
        return [{"error": str(e)}]


@mcp.tool
def query_funds_flow(
    size: int = 100,
    start_time: str = "",
    end_time: str = "",
) -> list[dict[str, Any]]:
    """Query funds flow.

    Args:
        size: Number of records to query (default: 100)
        start_time: Start time in format "YYYY-MM-DD" (default: 30 days ago)
        end_time: End time in format "YYYY-MM-DD" (default: today)

    Returns:
        List of funds flow records
    """
    try:
        client = get_client()

        # Set default dates if not provided
        if not start_time:
            start_time = (datetime.now()).strftime("%Y-%m-%d")
        if not end_time:
            end_time = (datetime.now()).strftime("%Y-%m-%d")

        result = client.query_funds_flow(size, start_time, end_time)
        data = _extract_data(result)
        return data if isinstance(data, list) else []
    except EmtlException as e:
        return [{"error": str(e)}]
    except ValueError as e:
        return [{"error": str(e)}]


@mcp.tool
def create_order(
    stock_code: str,
    trade_type: str,
    market: str,
    price: float,
    amount: int,
) -> dict[str, Any]:
    """Create a new order.

    Args:
        stock_code: Stock code (e.g., "600000")
        trade_type: Trade type - "B" for buy, "S" for sell
        market: Market code (e.g., "HA" for Shanghai A-share)
        price: Order price
        amount: Order amount (number of shares)

    Returns:
        Order creation result
    """
    try:
        client = get_client()
        result = client.create_order(stock_code, trade_type, market, price, amount)
        return _extract_data(result) or {}
    except EmtlException as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool
def cancel_order(order_str: str) -> dict[str, Any]:
    """Cancel an existing order.

    Args:
        order_str: Order ID string to cancel

    Returns:
        Order cancellation result
    """
    try:
        client = get_client()
        result = client.cancel_order(order_str)
        return _extract_data(result) or {}
    except EmtlException as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
