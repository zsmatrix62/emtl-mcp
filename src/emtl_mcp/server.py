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


@mcp.tool
def login(duration: int = 180) -> str:
    """Login to East Money trading platform using configured credentials.

    Note: This tool is provided for testing. The client automatically logs in
    when you use any other tool. You don't need to call this explicitly.

    Args:
        duration: Session duration in minutes (default: 180)

    Returns:
        Login status message
    """
    try:
        username, _ = get_credentials()
        client = get_client()
        return f"Successfully logged in as {username}"
    except LoginFailedError as e:
        return f"Login failed: {e}"
    except EmtlException as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Configuration error: {e}"


@mcp.tool
def query_asset_and_position() -> dict[str, Any]:
    """Query account assets and positions.

    Returns:
        Dictionary containing account assets and position information
    """
    try:
        client = get_client()
        result = client.query_asset_and_position()
        return result
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
        return result
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
        return result
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
        return result
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
        return result
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
        return result
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
        return result
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
        return result
    except EmtlException as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool
def get_last_price(symbol_code: str, market: str) -> dict[str, Any]:
    """Get the latest stock price.

    Args:
        symbol_code: Stock symbol code
        market: Market code

    Returns:
        Latest stock price information
    """
    try:
        client = get_client()
        result = client.get_last_price(symbol_code, market)
        return result
    except EmtlException as e:
        return {"error": str(e)}
    except ValueError as e:
        return {"error": str(e)}


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
