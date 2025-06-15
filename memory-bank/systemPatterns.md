# System Patterns: MCP Architecture & Design

## MCP Architecture Overview

### Client-Server Model

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Transport Layer │◄──►│   MCP Server    │
│ (EnhancedMCP)   │    │   (stdio/http)   │    │ (filesystem)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Key Components**:

- **Client**: Initiates connections, executes tools, manages resources
- **Transport**: Communication layer (stdio for local, HTTP for remote)
- **Server**: Provides tools and resources, handles requests

### Multi-Server Architecture

```
                    ┌─────────────────────┐
                    │  EnhancedMCPClient  │
                    │                     │
                    │  ┌─────────────────┐│
                    │  │ ConfigManager   ││
                    │  └─────────────────┘│
                    │  ┌─────────────────┐│
                    │  │ SessionManager  ││
                    │  └─────────────────┘│
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│ Filesystem  │    │   Math Server   │    │ Future HTTP │
│   Server    │    │   (Python)      │    │   Server    │
│   (NPX)     │    │                 │    │             │
└─────────────┘    └─────────────────┘    └─────────────┘
```

## Core Design Patterns

### 1. Configuration Management Pattern

**Pattern**: Centralized configuration with type safety
**Implementation**: `MCPConfigManager` + `MCPServerConfig` dataclass

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
        self.servers = {
            "filesystem": MCPServerConfig(...),
            "local-math": MCPServerConfig(...),
        }
```

**Benefits**:

- Type safety with dataclasses
- Centralized server definitions
- Easy addition of new servers
- Environment-specific configurations

### 2. Connection Lifecycle Management

**Pattern**: AsyncExitStack for resource management
**Implementation**: Automatic cleanup of subprocess connections

```python
class EnhancedMCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.sessions: Dict[str, ClientSession] = {}

    async def connect(self, server_name: str):
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        session = await self.exit_stack.enter_async_context(
            ClientSession(stdio, write)
        )
```

**Benefits**:

- Automatic resource cleanup
- Exception-safe connection handling
- Proper subprocess lifecycle management
- Memory leak prevention

### 3. Session Management Pattern

**Pattern**: Dictionary-based session registry with metadata
**Implementation**: Track both sessions and server configurations

```python
self.sessions: Dict[str, ClientSession] = {}
self.active_servers: Dict[str, MCPServerConfig] = {}
```

**Benefits**:

- Fast session lookup by server name
- Metadata available for debugging
- Easy iteration over active connections
- Clean separation of concerns

### 4. Tool Execution Pattern

**Pattern**: Server-scoped tool execution with error handling
**Implementation**: Validate connection before tool execution

```python
async def execute_tool(self, server_name: str, tool_name: str, args: Dict[str, Any]):
    if server_name not in self.sessions:
        raise ValueError(f"Not connected to {server_name}")

    session = self.sessions[server_name]
    try:
        result = await session.call_tool(tool_name, args)
        return result
    except Exception as e:
        logger.debug(f"Error executing {tool_name} on {server_name}: {e}")
        raise
```

**Benefits**:

- Clear error messages for connection issues
- Consistent error handling across tools
- Logging for debugging
- Type-safe argument passing

## Transport Patterns

### 1. Stdio Transport (Current)

**Use Case**: Local servers (Python scripts, NPX packages)
**Pattern**: Subprocess communication via stdin/stdout
**Implementation**: `StdioServerParameters` + `stdio_client`

```python
server_params = StdioServerParameters(
    command=config.command,
    args=config.args,
    env=config.env
)
stdio_transport = await stdio_client(server_params)
```

**Characteristics**:

- ✅ Low latency (local process)
- ✅ No network dependencies
- ✅ Secure (no external connections)
- ⚠️ Platform-specific subprocess handling
- ⚠️ Cleanup complexity on Windows

### 2. HTTP Transport (Future)

**Use Case**: Remote servers, cloud services, APIs
**Pattern**: HTTP-based communication
**Implementation**: Planned for future expansion

**Characteristics**:

- ✅ Network-accessible servers
- ✅ Standard HTTP protocols
- ✅ Scalable architecture
- ⚠️ Network latency considerations
- ⚠️ Authentication/security requirements

## Error Handling Patterns

### 1. Layered Error Handling

**Pattern**: Different error types at different layers

```
Application Layer    → ValueError for business logic errors
Client Layer        → ConnectionError for transport issues
Transport Layer     → subprocess.CalledProcessError for process issues
Protocol Layer      → MCP protocol errors
```

### 2. Graceful Degradation

**Pattern**: Continue operation when individual servers fail

```python
async def connect_all_servers(self):
    for server_name in self.config_manager.list_servers():
        try:
            await self.connect(server_name)
        except Exception as e:
            logger.warning(f"Failed to connect to {server_name}: {e}")
            # Continue with other servers
```

### 3. Resource Cleanup on Error

**Pattern**: Ensure cleanup even when errors occur

```python
try:
    # Server operations
    pass
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise
finally:
    await self.cleanup()
```

## Testing Patterns

### 1. Integration Testing Strategy

**Pattern**: Test real server connections rather than mocks
**Rationale**: MCP integration complexity requires end-to-end validation

```python
async def test_math_operations(self):
    await self.client.connect("local-math")
    result = await self.client.execute_tool("local-math", "add", {"a": 5, "b": 3})
    assert result.content[0].text == "8"
```

### 2. Test Lifecycle Management

**Pattern**: Proper setup/teardown with resource cleanup

```python
class MCPToolTester:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
```

### 3. Test Artifact Management

**Pattern**: Create and clean up test files

```python
# Create test file
await self.client.execute_tool("filesystem", "write_file", {
    "path": "test_file.txt",
    "content": "test content"
})

# Clean up in teardown
await self.client.execute_tool("filesystem", "delete_file", {
    "path": "test_file.txt"
})
```

## Logging Patterns

### 1. Structured Logging

**Pattern**: Consistent log format with context

```python
logger.debug(f"Connecting to {config.name}: {config.description}")
logger.debug(f"Available tools: {[tool.name for tool in tools]}")
logger.debug(f"Error executing {tool_name} on {server_name}: {e}")
```

### 2. Debug Context

**Pattern**: Include relevant context in debug messages

```python
current_dir = os.getcwd()
logger.debug("Enhanced MCP Client Initialised")
logger.debug(f"Current directory {current_dir}")
```

## Future Architecture Considerations

### 1. Connection Pooling

**Pattern**: Reuse connections for performance
**Implementation**: Pool of connections per server type

### 2. Async Resource Management

**Pattern**: Better async cleanup patterns
**Implementation**: Context managers for all async resources

### 3. Plugin Architecture

**Pattern**: Pluggable server types
**Implementation**: Registry pattern for transport types

### 4. Configuration Validation

**Pattern**: Validate configurations before use
**Implementation**: Pydantic models for config validation

## Key Architectural Decisions

### 1. Single Client, Multiple Servers

**Decision**: One client instance manages all server connections
**Rationale**: Simpler resource management, centralized logging
**Trade-off**: Potential single point of failure vs. complexity

### 2. Dataclass Configuration

**Decision**: Use dataclasses for server configuration
**Rationale**: Type safety, IDE support, clear structure
**Trade-off**: Python 3.7+ requirement vs. flexibility

### 3. AsyncExitStack Resource Management

**Decision**: Use AsyncExitStack for connection cleanup
**Rationale**: Automatic cleanup, exception safety
**Trade-off**: Learning curve vs. manual resource management

### 4. Integration Testing Focus

**Decision**: Emphasize integration tests over unit tests
**Rationale**: MCP complexity requires end-to-end validation
**Trade-off**: Slower tests vs. confidence in integration
