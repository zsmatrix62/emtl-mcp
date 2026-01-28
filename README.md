# EMTL MCP Server

MCP server for [East Money Trading Library (emtl)](https://github.com/zsmatrix62/emtl) - provides access to 东方财富持仓和历史交易数据.

## Features

- **Account Management**: Login to East Money trading platform
- **Asset Queries**: Query account assets and positions
- **Order Management**: Query current orders, create and cancel orders
- **Trade History**: Query historical orders and trades
- **Funds Flow**: Query funds flow records
- **Real-time Quotes**: Get latest stock prices
- **Secure Credentials**: Credentials stored in MCP config, never passed to LLM

## Installation

### Using uvx (recommended for production)

```bash
uvx emtl-mcp
```

### Local development

```bash
# Clone the repository
git clone https://github.com/your-org/emtl-mcp.git
cd emtl-mcp

# Install dependencies
uv sync

# Install local emtl for development
uv pip install -e /Users/kylehuang/dev/emtl

# Run the server
uv run python -m emtl_mcp.server
```

## Configuration

### Environment Variables

Configure credentials using environment variables in your MCP server configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| `EMTL_USERNAME` | East Money account username | Yes |
| `EMTL_PASSWORD` | East Money account password | Yes |
| `EMTL_STORAGE_DIR` | Cache storage directory (default: `./emtl-cache`) | No |

**Important**: Credentials are configured in the MCP server configuration, **not** passed to the LLM. This keeps your credentials secure.

## MCP Client Configuration

### Claude Code (stdio)

Edit `~/.claude/settings.json` or use Claude Code settings UI:

```json
{
  "mcpServers": {
    "emtl": {
      "command": "uvx",
      "args": ["emtl-mcp"],
      "env": {
        "EMTL_USERNAME": "your_username_here",
        "EMTL_PASSWORD": "your_password_here"
      }
    }
  }
}
```

### Local Development (Claude Code)

```json
{
  "mcpServers": {
    "emtl": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/kylehuang/dev/emtl-mcp",
        "run",
        "python",
        "-m",
        "emtl_mcp.server"
      ],
      "env": {
        "EMTL_USERNAME": "your_username_here",
        "EMTL_PASSWORD": "your_password_here"
      }
    }
  }
}
```

### Other MCP Clients (HTTP/SSE)

For HTTP/SSE transport, deploy as a web service:

```json
{
  "mcpServers": {
    "emtl": {
      "type": "streamable_http",
      "url": "http://localhost:8000/sse",
      "env": {
        "EMTL_USERNAME": "your_username_here",
        "EMTL_PASSWORD": "your_password_here"
      }
    }
  }
}
```

### Cursor IDE

Add to Cursor settings (`settings.json`):

```json
{
  "mcpServers": {
    "emtl": {
      "command": "uvx",
      "args": ["emtl-mcp"],
      "env": {
        "EMTL_USERNAME": "your_username_here",
        "EMTL_PASSWORD": "your_password_here"
      }
    }
  }
}
```

### Cline (Claude Dev)

Add to Cline settings:

```json
{
  "mcpServers": {
    "emtl": {
      "command": "uvx",
      "args": ["emtl-mcp"],
      "env": {
        "EMTL_USERNAME": "your_username_here",
        "EMTL_PASSWORD": "your_password_here"
      }
    }
  }
}
```

## MCP Tools

All tools use credentials configured in the MCP server environment. No need to pass username/password to the LLM.

### Authentication

#### `login(duration=180)`
Login to East Money trading platform using configured credentials.

**Note**: This tool is provided for testing. The client automatically logs in when you use any other tool.

### Query Functions

#### `query_asset_and_position()`
Query account assets and positions.

#### `query_orders()`
Query current pending orders.

#### `query_trades()`
Query trade records.

#### `query_history_orders(size=100, start_time="", end_time="")`
Query historical orders.

- `size`: Number of records to query (default: 100)
- `start_time`: Start time in format "YYYY-MM-DD" (default: today)
- `end_time`: End time in format "YYYY-MM-DD" (default: today)

#### `query_history_trades(size=100, start_time="", end_time="")`
Query historical trades.

#### `query_funds_flow(size=100, start_time="", end_time="")`
Query funds flow records.

### Trading Functions

#### `create_order(stock_code, trade_type, market, price, amount)`
Create a new order.

- `stock_code`: Stock code (e.g., "600000")
- `trade_type`: "B" for buy, "S" for sell
- `market`: Market code (e.g., "HA" for Shanghai A-share)
- `price`: Order price
- `amount`: Order amount (number of shares)

#### `cancel_order(order_str)`
Cancel an existing order.

### Quote Functions

#### `get_last_price(symbol_code, market)`
Get the latest stock price.

## Development

### Test the server

```bash
cd /Users/kylehuang/dev/emtl-mcp
./test_mcp.sh
```

### Manual testing with credentials

```bash
# Set credentials
export EMTL_USERNAME="your_username"
export EMTL_PASSWORD="your_password"

# Run server
uv run python -m emtl_mcp.server
```

## Security Notes

- ✅ **Credentials are stored in MCP configuration** - never passed to LLM
- ✅ **Sessions are cached** - reduces login frequency
- ✅ **Cache is stored locally** - in `EMTL_STORAGE_DIR` directory
- ⚠️ **Never share your Claude settings file** - it contains your credentials
- ⚠️ **Use environment variables** - don't hardcode credentials in code

## License

MIT

## References

- [emtl library](https://github.com/zsmatrix62/emtl)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
