# Technical Context: Technologies & Implementation

## Core Technologies

### Model Context Protocol (MCP)

**Version**: Latest (1.9.3 as of implementation)
**Purpose**: Standardized protocol for AI assistants to connect with external data sources and tools
**Documentation**: https://modelcontextprotocol.io/

**Key Concepts**:

- **Servers**: Provide tools and resources (filesystem, APIs, databases)
- **Clients**: Consume server capabilities (AI assistants, custom applications)
- **Transport**: Communication layer (stdio, HTTP, WebSocket)
- **Tools**: Executable functions with defined schemas
- **Resources**: Data sources that can be read or subscribed to

### Python MCP SDK

**Package**: `mcp` (official Python SDK)
**Installation**: `pip install mcp`
**Key Components**:

- `ClientSession`: Manages MCP client connections
- `StdioServerParameters`: Configuration for stdio-based servers
- `stdio_client`: Factory for stdio transport connections

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
```

### Python Asyncio

**Version**: Python 3.12.9 built-in asyncio
**Usage**: Asynchronous I/O for MCP client operations
**Key Patterns**:

- `AsyncExitStack`: Resource management for async contexts
- `asyncio.run()`: Entry point for async applications
- Subprocess management via `stdio_client`

**Windows Considerations**:

- Uses `ProactorEventLoop` by default
- Subprocess cleanup requires careful handling
- Event loop closure timing affects resource cleanup

## Development Environment

### Platform Specifications

- **OS**: Windows 10
- **Python**: 3.12.9 (via uv Python distribution)
- **Shell**: PowerShell 7
- **IDE**: VS Code with Python extension

### Virtual Environment

```bash
# Environment activation
(env) (base) PS D:\dev\Coursera\Agents\thales\src>

# Key packages installed
pip install mcp
pip install python-dotenv
pip install anthropic  # (commented out in current implementation)
```

### Project Structure

```
thales/
├── memory-bank/           # Memory bank documentation
├── src/
│   ├── debug.log         # Debug output
│   ├── mcp_test_file.txt # Test artifacts
│   └── thales/
│       ├── main.py       # Main application entry
│       ├── mcp/          # MCP implementation
│       │   ├── client/   # Custom MCP client
│       │   ├── server/   # Server configs and local servers
│       │   └── tests/    # Test suites
│       └── utils/        # Utilities (logging, etc.)
```

## MCP Server Configurations

### 1. Filesystem Server (NPX)

**Type**: Official MCP server via NPX
**Command**: `npx -y @modelcontextprotocol/server-filesystem`
**Scope**: `D:/dev/Coursera/Agents/thales` (project directory only)

**Configuration**:

```python
MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "D:/dev/Coursera/Agents/thales"],
    description="Official filesystem server with secure file operations"
)
```

**Available Tools**:

- `read_file`: Read file contents
- `write_file`: Create/overwrite files
- `list_directory`: List directory contents
- `create_directory`: Create directories
- `delete_file`: Delete files
- `move_file`: Move/rename files
- `search_files`: Search for files by pattern
- `get_file_info`: Get file metadata

### 2. Local Math Server (Python)

**Type**: Custom Python MCP server
**Command**: `python`
**Script**: `D:\dev\Coursera\Agents\thales\src\thales\mcp\server\math_server.py`

**Configuration**:

```python
MCPServerConfig(
    name="local-math",
    command="python",
    args=["D:\\dev\\Coursera\\Agents\\thales\\src\\thales\\mcp\\server\\math_server.py"],
    description="Local math operations server"
)
```

**Available Tools**:

- `add`: Addition operations
- `subtract`: Subtraction operations
- `multiply`: Multiplication operations
- `divide`: Division operations
- `power`: Exponentiation
- `sqrt`: Square root
- `factorial`: Factorial calculation

## Implementation Architecture

### Configuration Management

**File**: `thales/src/thales/mcp/server/mcp_config.py`
**Pattern**: Dataclass-based configuration with centralized registry

```python
@dataclass
class MCPServerConfig:
    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    description: str = ""

class MCPConfigManager:
    def __init__(self):
        self.servers = {...}  # Server registry
```

### Client Implementation

**File**: `thales/src/thales/mcp/client/client.py`
**Pattern**: Single client managing multiple server connections

**Key Features**:

- Async connection management with `AsyncExitStack`
- Session registry with metadata tracking
- Tool execution with error handling
- Interactive mode for testing
- Integrated logging for debugging

### Testing Framework

**File**: `thales/src/thales/mcp/tests/test_enhanced_client.py`
**Pattern**: Integration testing with real server connections

**Test Categories**:

- Configuration validation
- Server connection testing
- Tool execution validation
- Resource cleanup verification
- Error handling scenarios

## Technical Constraints & Considerations

### Security Constraints

- **Filesystem Access**: Limited to project directory only
- **Command Execution**: Only configured servers can be executed
- **Network Access**: Currently no HTTP servers configured
- **Process Isolation**: Each server runs in separate subprocess

### Performance Considerations

- **Connection Overhead**: Each server requires subprocess startup
- **Memory Usage**: Multiple concurrent server processes
- **Cleanup Timing**: Proper resource cleanup to prevent leaks
- **Error Recovery**: Graceful handling of server failures

### Platform-Specific Issues

- **Windows Asyncio**: ProactorEventLoop subprocess cleanup timing
- **Path Handling**: Absolute paths required for reliability
- **Process Management**: Subprocess lifecycle on Windows
- **File System**: Windows path separators in configuration

## Dependencies & Requirements

### Core Dependencies

```python
# MCP SDK
mcp>=1.9.3

# Async utilities
asyncio  # Built-in

# Configuration
python-dotenv
typing  # Built-in
dataclasses  # Built-in

# Logging
logging  # Built-in (custom logger wrapper)
```

### Development Dependencies

```python
# Testing (implicit - using built-in unittest patterns)
pytest  # Not currently used but recommended for future

# Code quality
black   # For formatting (evident from auto-formatting)
mypy    # For type checking (recommended)
```

### Optional Dependencies

```python
# AI integration (commented out)
anthropic  # For future AI assistant integration

# Additional servers
requests   # For HTTP-based MCP servers
websockets # For WebSocket-based MCP servers
```

## Configuration Files

### Environment Configuration

**File**: `.env` (project root)
**Purpose**: Environment variables for API keys and configuration
**Status**: Present but contents not specified in current implementation

### Cline MCP Settings

**File**: `c:/Users/kaiha/AppData/Roaming/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
**Purpose**: Configure MCP servers for Cline integration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "d:/dev/Coursera/Agents"],
      "disabled": false,
      "autoApprove": []
    },
    "local-math": {
      "command": "python",
      "args": ["d:/dev/Coursera/Agents/mcp/server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Logging & Debugging

### Custom Logger

**File**: `thales/src/thales/utils/logger/logger.py`
**Usage**: Centralized logging for MCP operations
**Integration**: Used throughout MCP client for debugging

**Log Levels**:

- `DEBUG`: Connection details, tool execution, server responses
- `INFO`: High-level operations and status
- `WARNING`: Non-fatal issues and fallbacks
- `ERROR`: Failures and exceptions

### Debug Output

**File**: `thales/src/debug.log`
**Content**: Runtime debug information from MCP operations
**Usage**: Troubleshooting connection and execution issues

## Testing Infrastructure

### Test Execution

**Command**: `python -m thales.mcp.tests.test_enhanced_client`
**Working Directory**: `thales/src/`
**Environment**: Virtual environment with MCP SDK installed

### Test Artifacts

- **Created Files**: `mcp_test_file.txt` (filesystem server test)
- **Log Output**: Debug information to console and log files
- **Cleanup**: Automatic cleanup of test files (when possible)

### Known Test Issues

- **Asyncio Cleanup Warnings**: Cosmetic subprocess cleanup warnings on Windows
- **Resource Management**: Need for explicit cleanup sequences
- **Error Handling**: Some edge cases not fully covered

## Future Technical Considerations

### Planned Enhancements

- **HTTP Transport**: Support for remote MCP servers
- **Connection Pooling**: Reuse connections for performance
- **Configuration Validation**: Pydantic models for config validation
- **Enhanced Error Handling**: More robust error recovery patterns

### Scalability Considerations

- **Multi-threading**: Concurrent server operations
- **Resource Limits**: Memory and process limits for servers
- **Monitoring**: Health checks and performance metrics
- **Caching**: Response caching for expensive operations

### Integration Opportunities

- **AI Assistant Integration**: Anthropic Claude integration
- **Database Servers**: SQL and NoSQL database MCP servers
- **API Servers**: REST API and GraphQL MCP servers
- **Cloud Services**: AWS, Azure, GCP MCP server integrations
