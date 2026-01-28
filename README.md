# EMTL MCP Server

MCP 服务器，用于 [East Money Trading Library (emtl)](https://github.com/zsmatrix62/emtl) - 提供东方财富持仓和历史交易数据访问。

## 功能特性

- **资产查询**: 查询账户资产和持仓
- **订单管理**: 查询当前委托、创建和撤销订单
- **交易历史**: 查询历史订单和成交记录
- **资金流水**: 查询资金流水记录
- **字段缩写**: 查询字段名称映射（中文/英文）
- **安全凭证**: 凭证存储在 MCP 配置中，不会传递给 LLM
- **自动登录**: 首次使用时自动登录

## 安装

### 生产环境（从 Git 安装）

使用 `uvx` 通过 Git URL 安装：

```bash
uvx --from git+https://github.com/your-org/emtl-mcp.git emtl-mcp
```

或克隆后运行：

```bash
git clone https://github.com/your-org/emtl-mcp.git
cd emtl-mcp
uv run python -m emtl_mcp.server
```

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/your-org/emtl-mcp.git
cd emtl-mcp

# 安装依赖
uv sync

# 安装本地 emtl 开发版本
uv pip install -e ~/dev/emtl

# 运行服务器
uv run python -m emtl_mcp.server
```

## 配置

### 环境变量

在 MCP 服务器配置中使用环境变量配置凭证：

| 变量               | 说明                                 | 必填 |
| ------------------ | ------------------------------------ | ---- |
| `EMTL_USERNAME`    | 东方财富账号用户名                   | 是   |
| `EMTL_PASSWORD`    | 东方财富账号密码                     | 是   |
| `EMTL_STORAGE_DIR` | 缓存存储目录（默认：`./emtl-cache`） | 否   |

**重要提示**: 凭证在 MCP 服务器配置中设置，**不会**传递给 LLM。这样可以保护您的凭证安全。

## Claude Code 配置

### 生产环境（从 Git 安装）

编辑 `~/.claude/settings.json`：

```json
{
  "mcpServers": {
    "emtl": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/zsmatrix62/emtl-mcp.git",
        "emtl-mcp"
      ],
      "env": {
        "EMTL_USERNAME": "你的用户名",
        "EMTL_PASSWORD": "你的密码"
      }
    }
  }
}
```

### 本地开发

```json
{
  "mcpServers": {
    "emtl": {
      "command": "uv",
      "args": [
        "--directory",
        "~/dev/emtl-mcp",
        "run",
        "python",
        "-m",
        "emtl_mcp.server"
      ],
      "env": {
        "EMTL_USERNAME": "你的用户名",
        "EMTL_PASSWORD": "你的密码"
      }
    }
  }
}
```

## MCP 工具

所有工具都使用 MCP 服务器环境中配置的凭证。无需向 LLM 传递用户名/密码。

首次调用任何工具时，客户端会自动登录。

### 查询工具

#### `query_asset_and_position()`

查询账户资产和持仓。

返回包含以下内容的字典：

- 账户摘要（总资产、可用资金等）
- 持仓股票列表

#### `query_orders()`

查询当前委托订单。

#### `query_trades()`

查询成交记录。

#### `query_history_orders(size=100, start_time="", end_time="")`

查询历史订单。

- `size`: 查询记录数量（默认：100）
- `start_time`: 开始时间，格式 "YYYY-MM-DD"（默认：今天）
- `end_time`: 结束时间，格式 "YYYY-MM-DD"（默认：今天）

#### `query_history_trades(size=100, start_time="", end_time="")`

查询历史成交记录。

#### `query_funds_flow(size=100, start_time="", end_time="")`

查询资金流水记录。

#### `query_abbrs(keys="")`

查询字段缩写映射。

此工具帮助您理解 API 响应中缩写字段的含义。

- `keys`: 要查询的缩写键，用逗号分隔（可选）
  - 如果为空，返回所有缩写
  - 示例：`"Zqdm,Zqmc"` 查询股票代码和股票名称

返回包含每个缩写的中文名称和英文描述的字典。

使用示例：

```python
# 获取所有缩写
query_abbrs()

# 获取特定缩写
query_abbrs("Zqdm,Zqmc,Wtsl")
```

### 交易工具

#### `create_order(stock_code, trade_type, market, price, amount)`

创建新订单。

- `stock_code`: 股票代码（如 "600000"）
- `trade_type`: 交易类型，买入为 "B"，卖出为 "S"
- `market`: 市场代码（如沪A为 "HA"）
- `price`: 委托价格
- `amount`: 委托数量（股数）

#### `cancel_order(order_str)`

撤销现有订单。

## 开发

### 测试服务器

```bash
cd ~/dev/emtl-mcp
./test_mcp.sh
```

### 手动测试（带凭证）

```bash
# 设置凭证
export EMTL_USERNAME="你的用户名"
export EMTL_PASSWORD="你的密码"

# 运行服务器
uv run python -m emtl_mcp.server
```

## 安全提示

- ✅ **凭证存储在 MCP 配置中** - 不会传递给 LLM
- ✅ **会话已缓存** - 减少登录频率
- ✅ **缓存存储在本地** - 位于 `EMTL_STORAGE_DIR` 目录
- ✅ **首次使用时自动登录** - 无需手动登录
- ⚠️ **切勿分享您的 Claude 设置文件** - 其中包含您的凭证
- ⚠️ **使用环境变量** - 不要在代码中硬编码凭证

## 许可证

MIT

## 相关链接

- [emtl 库](https://github.com/zsmatrix62/emtl)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
