#!/bin/bash
# Test script to verify MCP server configuration

echo "Testing EMTL MCP Server..."
echo ""

# Check if project directory exists
if [ ! -d "/Users/kylehuang/dev/emtl-mcp" ]; then
    echo "❌ Project directory not found"
    exit 1
fi

echo "✅ Project directory exists"

# Check if virtual environment exists
if [ ! -d "/Users/kylehuang/dev/emtl-mcp/.venv" ]; then
    echo "❌ Virtual environment not found. Run: uv sync"
    exit 1
fi

echo "✅ Virtual environment exists"

# Check if emtl is installed
echo ""
echo "Checking emtl installation..."
/Users/kylehuang/dev/emtl-mcp/.venv/bin/python -c "import emtl; print(f'✅ emtl version: {emtl.__version__}')" 2>/dev/null || {
    echo "❌ emtl not installed. Run: uv pip install -e /Users/kylehuang/dev/emtl"
    exit 1
}

# Check if server can be imported
echo ""
echo "Checking MCP server..."
/Users/kylehuang/dev/emtl-mcp/.venv/bin/python -c "
from emtl_mcp.server import mcp
print(f'✅ MCP server loaded: {mcp.name}')
print(f'✅ Tools available: {len(list(mcp._tool_manager._tools.values()))}')
print('')
print('Available tools (no credentials required):')
for tool in mcp._tool_manager._tools.values():
    print(f'  - {tool.name}')
" || {
    echo "❌ Failed to load MCP server"
    exit 1
}

echo ""
echo "✅ All checks passed!"
echo ""
echo "IMPORTANT: Credentials are configured via environment variables!"
echo ""
echo "Add this to your Claude Code config (~/.claude/settings.json):"
echo ""
cat << 'EOF'
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
EOF
echo ""
echo "⚠️  Replace 'your_username_here' and 'your_password_here' with your actual credentials."
echo "⚠️  Never share your Claude settings file with others."
