# Technical Context: Modular AI Agent Framework Technologies

## Core Technologies Overview

### Model Context Protocol (MCP) - Foundation Layer

**Version**: Latest (1.9.3 as of implementation)
**Purpose**: Tool integration layer for AI agents
**Status**: Foundation complete, production ready
**Documentation**: https://modelcontextprotocol.io/

**Key Concepts**:
- **Servers**: Provide tools and resources (filesystem, APIs, databases)
- **Clients**: Consume server capabilities (AI assistants, custom applications)
- **Transport**: Communication layer (stdio, HTTP, WebSocket)
- **Tools**: Executable functions with defined schemas
- **Resources**: Data sources that can be read or subscribed to

**Role in Agent Framework**: MCP serves as the tool discovery and execution layer, allowing agents to dynamically discover and use available tools.

### Python MCP SDK

**Package**: `mcp` (official Python SDK)
**Installation**: `pip install mcp`
**Status**: Production ready, extensively tested
**Key Components**:

- `ClientSession`: Manages MCP client connections
- `StdioServerParameters`: Configuration for stdio-based servers
- `stdio_client`: Factory for stdio transport connections

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
```

## Agent Framework Technologies (Planned)

### Large Language Model Integration

**Purpose**: Core reasoning and natural language processing for agents
**Status**: Design phase
**Planned Providers**:

#### OpenAI Integration
```python
# Planned implementation
from openai import AsyncOpenAI

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
```

**Models**:
- **GPT-4**: Complex reasoning, goal decomposition
- **GPT-3.5-turbo**: Fast responses, simple tasks
- **GPT-4-turbo**: Cost-effective for high-volume operations

#### Anthropic Integration
```python
# Planned implementation
from anthropic import AsyncAnthropic

class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
```

**Models**:
- **Claude-3-Opus**: Highest capability for complex reasoning
- **Claude-3-Sonnet**: Balanced performance and cost
- **Claude-3-Haiku**: Fast responses for simple tasks

#### Local Model Support (Future)
```python
# Planned implementation
class OllamaClient(LLMClient):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
```

**Benefits**:
- Privacy and data control
- No API costs
- Offline operation
- Custom fine-tuned models

### Knowledge Graph Technologies

**Purpose**: Advanced context retrieval and relationship modeling
**Status**: Design phase

#### Neo4j Integration
```python
# Planned implementation
from neo4j import AsyncGraphDatabase

class Neo4jDatabase(GraphDatabase):
    def __init__(self, uri: str, username: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(username, password))
```

**Use Cases**:
- Entity relationship modeling
- Complex query traversal
- Knowledge graph construction
- Semantic memory storage

#### Vector Database Integration
```python
# Planned implementation options
from chromadb import AsyncClient as ChromaClient
from pinecone import Pinecone
from weaviate import Client as WeaviateClient

class VectorStore:
    async def similarity_search(self, query: str, k: int = 10) -> List[SearchResult]:
        # Vector similarity search implementation
        pass
```

**Planned Providers**:
- **ChromaDB**: Local vector storage, easy setup
- **Pinecone**: Managed vector database, high performance
- **Weaviate**: Open source, GraphQL interface
- **FAISS**: Facebook's similarity search library

### Memory System Technologies

**Purpose**: Agent working memory and long-term knowledge storage
**Status**: Design phase

#### Working Memory (In-Memory)
```python
# Planned implementation
import asyncio
from datetime import datetime, timedelta

class WorkingMemory:
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.memory: Dict[str, MemoryItem] = {}
        self.max_size = max_size
        self.ttl = timedelta(seconds=ttl_seconds)
```

**Technologies**:
- **Redis**: Distributed in-memory storage
- **Python dict**: Simple local storage
- **SQLite**: Persistent local storage

#### Semantic Memory (Graph + Vector)
```python
# Planned implementation
class SemanticMemory:
    def __init__(self, graph_db: GraphDatabase, vector_store: VectorStore):
        self.graph_db = graph_db
        self.vector_store = vector_store
```

**Technologies**:
- **Neo4j + ChromaDB**: Graph relationships + vector similarity
- **Knowledge Graph embeddings**: Node2Vec, Graph neural networks
- **Semantic indexing**: Automatic concept extraction and linking

## Development Environment

### Platform Specifications

- **OS**: Windows 10/11 (primary), Linux support planned
- **Python**: 3.12.9+ (async/await, dataclasses, type hints)
- **Shell**: PowerShell 7 (Windows), Bash (Linux)
- **IDE**: VS Code with Python extension, Jupyter notebooks for experimentation

### Virtual Environment Management

```bash
# Current setup
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux

# Package management
pip install -r requirements.txt
pip freeze > requirements.txt
```

### Project Structure (Expanded)

```
thales/
├── memory-bank/           # Memory bank documentation
├── src/
│   ├── thales/
│   │   ├── agents/        # Agent framework core (NEW)
│   │   │   ├── base/      # Base agent classes
│   │   │   ├── memory/    # Memory systems
│   │   │   ├── tools/     # Tool discovery engine
│   │   │   └── coordination/ # Multi-agent patterns
│   │   ├── llm/           # LLM abstraction layer (NEW)
│   │   │   ├── providers/ # LLM provider implementations
│   │   │   └── clients/   # LLM client interfaces
│   │   ├── rag/           # Knowledge Graph RAG (NEW)
│   │   │   ├── graph/     # Graph database interfaces
│   │   │   ├── vector/    # Vector store interfaces
│   │   │   └── search/    # Hybrid search engines
│   │   ├── mcp/           # MCP integration (COMPLETE)
│   │   │   ├── client/    # Custom MCP client
│   │   │   ├── server/    # Server configs and local servers
│   │   │   └── tests/     # Test suites
│   │   └── utils/         # Utilities (logging, config, etc.)
│   ├── tests/             # Package-level tests (NEW)
│   ├── examples/          # Usage examples (NEW)
│   └── docs/              # Documentation (NEW)
├── requirements.txt       # Dependencies
├── setup.py              # Package setup (NEW)
├── pyproject.toml        # Modern Python packaging (NEW)
└── README.md             # Project documentation
```

## Dependencies & Requirements

### Core Dependencies (Current)

```python
# MCP Foundation (Production Ready)
mcp>=1.9.3                    # Official MCP SDK
python-dotenv>=1.0.0          # Environment configuration
typing-extensions>=4.0.0      # Enhanced type hints

# Async utilities
asyncio                       # Built-in async framework
contextlib                    # AsyncExitStack for resource management
dataclasses                   # Built-in data structures
```

### Agent Framework Dependencies (Planned)

```python
# LLM Providers
openai>=1.0.0                 # OpenAI API client
anthropic>=0.8.0              # Anthropic API client
ollama>=0.1.0                 # Local model support (optional)

# Knowledge Graph & Vector Storage
neo4j>=5.0.0                  # Neo4j graph database
chromadb>=0.4.0               # Vector database
sentence-transformers>=2.0.0  # Text embeddings
numpy>=1.24.0                 # Numerical operations
```

### Development Dependencies (Planned)

```python
# Testing
pytest>=7.0.0                 # Testing framework
pytest-asyncio>=0.21.0        # Async test support
pytest-cov>=4.0.0             # Coverage reporting

# Code Quality
black>=23.0.0                 # Code formatting
mypy>=1.0.0                   # Type checking
flake8>=6.0.0                 # Linting
isort>=5.0.0                  # Import sorting

# Documentation
sphinx>=6.0.0                 # Documentation generation
sphinx-rtd-theme>=1.0.0       # ReadTheDocs theme
```

### Optional Dependencies (Future)

```python
# Enterprise Features
redis>=4.0.0                  # Distributed memory
celery>=5.0.0                 # Distributed task queue
prometheus-client>=0.16.0     # Metrics and monitoring

# Advanced Features
torch>=2.0.0                  # Deep learning (optional)
transformers>=4.0.0           # Hugging Face models
networkx>=3.0.0               # Graph algorithms
```

## Configuration Management

### Environment Configuration

**File**: `.env` (project root)
**Purpose**: API keys, database connections, feature flags

```bash
# LLM Provider Configuration
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_BASE_URL=http://localhost:11434

# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...

# Agent Configuration
DEFAULT_LLM_PROVIDER=openai
DEFAULT_LLM_MODEL=gpt-4
MAX_WORKING_MEMORY_SIZE=1000
SEMANTIC_MEMORY_TTL=86400
```

### Package Configuration

**File**: `pyproject.toml` (planned)
**Purpose**: Modern Python packaging configuration

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "thales-agents"
version = "0.1.0"
description = "Modular AI Agent Framework"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
dependencies = [
    "mcp>=1.9.3",
    "openai>=1.0.0",
    "anthropic>=0.8.0",
    "neo4j>=5.0.0",
    "chromadb>=0.4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
```

## MCP Server Configurations (Current - Production Ready)

### 1. Filesystem Server (NPX)

**Type**: Official MCP server via NPX
**Command**: `npx -y @modelcontextprotocol/server-filesystem`
**Scope**: Project directory only (security constraint)
**Status**: Production ready, extensively tested

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
- `read_file`, `write_file`, `list_directory`
- `create_directory`, `delete_file`, `move_file`
- `search_files`, `get_file_info`

### 2. Local Math Server (Python)

**Type**: Custom Python MCP server
**Status**: Production ready, comprehensive test coverage

**Available Tools**:
- `add`, `subtract`, `multiply`, `divide`
- `power`, `sqrt`, `factorial`

### 3. Context DB Server (Python)

**Type**: Custom Python MCP server
**Status**: Implemented, pending integration tests
**Purpose**: Provides persistent storage for agent context components (Identities, Goals, Tasks) using SQLite.

**Configuration**:
```python
MCPServerConfig(
    name="context-db",
    command="python",
    args=["D:\\dev\\Coursera\\Agents\\thales\\src\\thales\\mcp\\server\\context_db_server.py"],
    description="Server for storing and retrieving agent context components."
)
```

**Available Tools**:
- `store_identity`, `get_identity`
- `store_goal`, `get_goal`
- `store_task`, `get_task`
- `find_components`

## Planned MCP Server Integrations

### 4. Database Server (Planned)

**Purpose**: SQL and NoSQL database operations
**Implementation**: Custom MCP server with database connectors

```python
# Planned MCP server
class DatabaseServer:
    def __init__(self, connection_string: str):
        self.connection = create_connection(connection_string)
    
    async def execute_query(self, query: str, parameters: Dict = None):
        # Execute SQL query with parameters
        pass
```

### 4. API Server (Planned)

**Purpose**: REST API and GraphQL integrations
**Implementation**: HTTP client MCP server

```python
# Planned MCP server
class APIServer:
    def __init__(self, base_url: str, auth_config: Dict):
        self.base_url = base_url
        self.auth = setup_auth(auth_config)
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None):
        # Make HTTP request to API
        pass
```

## Testing Infrastructure

### Test Execution Environment

**Command**: `python -m pytest tests/`
**Working Directory**: `thales/src/`
**Environment**: Virtual environment with all dependencies

### Test Categories (Planned)

#### Unit Tests
```python
# Test individual components
pytest tests/unit/test_goal_processor.py
pytest tests/unit/test_tool_discovery.py
pytest tests/unit/test_memory_systems.py
```

#### Integration Tests
```python
# Test component interactions
pytest tests/integration/test_agent_execution.py
pytest tests/integration/test_mcp_integration.py
pytest tests/integration/test_llm_providers.py
```

#### End-to-End Tests
```python
# Test complete workflows
pytest tests/e2e/test_agent_workflows.py
pytest tests/e2e/test_multi_agent_coordination.py
```

### Performance Testing (Planned)

```python
# Performance benchmarks
pytest tests/performance/test_agent_response_time.py
pytest tests/performance/test_memory_performance.py
pytest tests/performance/test_concurrent_agents.py
```

## Logging & Monitoring

### Custom Logger (Current)

**File**: `thales/src/thales/utils/logger/logger.py`
**Status**: Production ready
**Usage**: Centralized logging for all components

**Log Levels**:
- `DEBUG`: Detailed execution information
- `INFO`: High-level operations and status
- `WARNING`: Non-fatal issues and fallbacks
- `ERROR`: Failures and exceptions
- `CRITICAL`: System-level failures

### Monitoring (Planned)

```python
# Planned monitoring integration
from prometheus_client import Counter, Histogram, Gauge

# Metrics collection
agent_executions = Counter('agent_executions_total', 'Total agent executions')
execution_duration = Histogram('agent_execution_duration_seconds', 'Agent execution time')
active_agents = Gauge('active_agents', 'Number of active agents')
```

## Security Considerations

### Current Security Measures

- **Filesystem Access**: Limited to project directory only
- **Command Execution**: Only configured MCP servers allowed
- **Process Isolation**: Each MCP server runs in separate subprocess
- **No Network Access**: Currently no HTTP-based servers configured

### Planned Security Enhancements

```python
# Planned security features
class SecurityManager:
    def __init__(self, policy_config: Dict):
        self.policies = load_security_policies(policy_config)
    
    async def validate_tool_execution(self, agent_id: str, tool_name: str, parameters: Dict) -> bool:
        # Validate tool execution against security policies
        pass
    
    async def audit_log(self, event: SecurityEvent):
        # Log security-relevant events
        pass
```

**Security Features**:
- **Role-Based Access Control**: Agent permissions and restrictions
- **Audit Logging**: Complete audit trail of agent actions
- **Resource Limits**: CPU, memory, and execution time limits
- **Sandboxing**: Isolated execution environments for agents

## Performance Considerations

### Current Performance Characteristics

- **MCP Connection Overhead**: ~100-200ms per server startup
- **Tool Execution**: <10ms for math operations, varies for filesystem
- **Memory Usage**: ~50MB base, +10MB per active MCP server
- **Cleanup Time**: ~1-2 seconds for graceful shutdown

### Planned Performance Optimizations

```python
# Connection pooling
class MCPConnectionPool:
    def __init__(self, max_connections: int = 10):
        self.pool = asyncio.Queue(maxsize=max_connections)
    
    async def get_connection(self, server_name: str) -> ClientSession:
        # Reuse existing connections
        pass

# Caching layer
class ResponseCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    async def get_cached_response(self, key: str) -> Optional[Any]:
        # Return cached response if valid
        pass
```

## Future Technical Considerations

### Scalability Enhancements

- **Distributed Agents**: Multi-process and multi-machine agent execution
- **Load Balancing**: Distribute agent workload across resources
- **Horizontal Scaling**: Add more agent instances as needed
- **Resource Management**: Dynamic resource allocation and limits

### Advanced Features

- **Agent Learning**: Reinforcement learning and experience replay
- **Custom Models**: Fine-tuned models for specific domains
- **Visual Interfaces**: Web-based agent configuration and monitoring
- **API Gateway**: RESTful API for external agent integration

### Integration Opportunities

- **Cloud Platforms**: AWS, Azure, GCP integration
- **Enterprise Systems**: LDAP, SSO, enterprise databases
- **Development Tools**: IDE plugins, CI/CD integration
- **Monitoring Systems**: Grafana, Datadog, New Relic integration

The technical foundation built with MCP provides an excellent base for the expanded Agent Framework, with proven patterns for tool integration, configuration management, testing, and resource management that will scale to support the full agent ecosystem.
