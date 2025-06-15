# Thales: Modular AI Agent Learning Project

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.9.3-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Learn AI Agents by building them** - A comprehensive educational project that evolves from MCP integration to a full-featured modular AI agent framework.

## 🎯 What This Project Is

**Thales** is a hands-on learning project that teaches AI agent development through progressive implementation. Starting with a solid Model Context Protocol (MCP) foundation, it evolves into a comprehensive agent framework supporting goal processing, tool discovery, knowledge graph RAG, and multi-agent coordination.

### 🚀 **What's Working Right Now**
- ✅ **Cline MCP Integration**: Immediate filesystem operations through Cline
- ✅ **Custom MCP Client**: Production-ready multi-server MCP client
- ✅ **Configuration Management**: Type-safe server configuration system
- ✅ **Comprehensive Testing**: Integration tests for all MCP operations
- ✅ **Tool Execution**: Math and filesystem operations validated

### 🔮 **Future Vision**
- 🎯 **Goal-Driven Agents**: Natural language goal → actionable tasks
- 🔧 **Dynamic Tool Discovery**: Automatic MCP server/tool selection
- 🧠 **Knowledge Graph RAG**: Advanced context retrieval using graph relationships
- 🤝 **Multi-Agent Coordination**: Collaborative agent workflows
- 📦 **Professional Package**: Deployable Python package for production use

## 📚 Educational Objectives

This project teaches through hands-on implementation:

- **MCP Protocol Fundamentals**: Client-server architecture, tool integration
- **Agent Design Patterns**: Goal processing, memory systems, coordination
- **Python Package Development**: Professional structure, testing, documentation
- **Knowledge Graph RAG**: Graph databases, vector search, semantic retrieval
- **Multi-Agent Systems**: Communication protocols, workflow orchestration
- **Production Best Practices**: Testing, logging, configuration management

## 🏗️ Architecture Overview

### Current Architecture (MCP Foundation - 85% Complete)

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Foundation (Working)                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Enhanced  │  │    MCP      │  │     Testing &       │  │
│  │ MCP Client  │  │ Config      │  │    Validation       │  │
│  │             │  │ Manager     │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Planned Architecture (Full Agent Framework)

```
┌─────────────────────────────────────────────────────────────────┐
│                 Modular AI Agent Framework                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Agent     │  │   Memory    │  │    RAG      │  │  Multi  │ │
│  │ Framework   │  │  Systems    │  │  Knowledge  │  │ Agent   │ │
│  │    Core     │  │             │  │   Graph     │  │Patterns │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │     LLM     │  │    Tool     │  │    MCP      │  │  Utils  │ │
│  │ Abstraction │  │ Discovery   │  │Foundation   │  │ & Core  │ │
│  │    Layer    │  │   Engine    │  │ (Complete)  │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js (for NPX-based MCP servers)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd thales
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your API keys for future LLM integration
   ```

### Try It Now - MCP Client

```bash
# Navigate to source directory
cd src

# Test the MCP client with math server
python -m thales.mcp.client.client local-math

# Or run comprehensive tests
python -m thales.mcp.tests.test_enhanced_client
```

### Immediate Value - Cline Integration

The project includes working Cline MCP integration for immediate filesystem operations:

- **Filesystem operations**: Read, write, list files through Cline
- **Math operations**: Calculator functions available in Cline
- **Secure access**: Limited to project directory for safety

## 📁 Project Structure

```
thales/
├── memory-bank/              # Project documentation and planning
│   ├── projectbrief.md      # Core objectives and strategy
│   ├── progress.md          # Current status and roadmap
│   ├── activeContext.md     # Current work focus
│   ├── productContext.md    # Product vision and value
│   ├── systemPatterns.md    # Architecture patterns
│   └── techContext.md       # Technical details
├── src/thales/
│   ├── mcp/                 # MCP Foundation (COMPLETE)
│   │   ├── client/          # Enhanced MCP client
│   │   ├── server/          # Server configurations
│   │   └── tests/           # Comprehensive test suite
│   ├── agents/              # Agent Framework (PLANNED)
│   │   ├── base/            # Base agent classes
│   │   ├── memory/          # Memory systems
│   │   ├── tools/           # Tool discovery engine
│   │   └── coordination/    # Multi-agent patterns
│   ├── llm/                 # LLM abstraction (PLANNED)
│   ├── rag/                 # Knowledge Graph RAG (PLANNED)
│   └── utils/               # Shared utilities
└── requirements.txt         # Dependencies
```

## 🔧 Current Features (MCP Foundation)

### Enhanced MCP Client

```python
from thales.mcp.client.client import EnhancedMCPClient

# Create client
client = EnhancedMCPClient()

# Connect to servers
await client.connect("filesystem")
await client.connect("local-math")

# Execute tools
result = await client.execute_tool("local-math", "add", {"a": 5, "b": 3})
print(result.content[0].text)  # "8"

# File operations
await client.execute_tool("filesystem", "write_file", {
    "path": "example.txt",
    "content": "Hello, MCP!"
})
```

### Configuration Management

```python
from thales.mcp.server.mcp_config import MCPConfigManager

# Centralized server configuration
config_manager = MCPConfigManager()

# Add new servers easily
config_manager.add_server("my-server", {
    "command": "python",
    "args": ["path/to/server.py"],
    "description": "My custom MCP server"
})
```

### Comprehensive Testing

```bash
# Run all MCP tests
python -m thales.mcp.tests.test_enhanced_client

# Test specific functionality
python -m thales.mcp.tests.test_config
```

## 🎯 Development Phases

### Phase A: MCP Foundation (85% Complete)
- ✅ **A1**: Cline MCP Integration - Immediate filesystem access
- ✅ **A2**: Configuration System - Centralized server management
- 🔧 **A3**: Enhanced Client - Multi-server MCP client (cleanup pending)
- 🔧 **A4**: Testing & Validation - Comprehensive test suite (minor issues)
- 📋 **A5**: Documentation - Usage guides and examples

### Phase B: Agent Framework Core (Planned)
- 📋 **B1**: Goal Processing System - Natural language → actionable tasks
- 📋 **B2**: Tool Discovery Engine - Dynamic MCP server/tool selection
- 📋 **B3**: Base Agent Classes - Core agent abstractions
- 📋 **B4**: LLM Abstraction Layer - Multi-provider support
- 📋 **B5**: Agent Memory Systems - Working + semantic memory

### Phase C: Knowledge Graph RAG (Planned)
- 📋 **C1**: Graph Integration - Neo4j, vector databases
- 📋 **C2**: RAG Agent - Specialized context retrieval agent
- 📋 **C3**: Semantic Search - Vector + graph hybrid search
- 📋 **C4**: Context Optimization - Relevance ranking
- 📋 **C5**: Graph Construction - Automated knowledge graphs

### Phase D: Multi-Agent Patterns (Planned)
- 📋 **D1**: Agent Communication - Inter-agent messaging
- 📋 **D2**: Coordination Patterns - Task distribution
- 📋 **D3**: Conflict Resolution - Resource management
- 📋 **D4**: Workflow Orchestration - Complex workflows
- 📋 **D5**: Performance Monitoring - Agent optimization

### Phase E: Package Development (Planned)
- 📋 **E1**: Package Structure - Professional organization
- 📋 **E2**: API Design - Clean public interfaces
- 📋 **E3**: Documentation - Comprehensive guides
- 📋 **E4**: Testing Suite - Full test coverage
- 📋 **E5**: Distribution - PyPI deployment

## 🧪 Testing

### Current Test Coverage

```bash
# MCP Foundation Tests
python -m thales.mcp.tests.test_config          # Configuration management
python -m thales.mcp.tests.test_enhanced_client # Client functionality

# Test Categories
- ✅ Configuration validation
- ✅ Server connection management
- ✅ Tool execution (math, filesystem)
- ✅ Error handling and edge cases
- ✅ Resource cleanup
```

### Planned Test Expansion

```bash
# Agent Framework Tests (Planned)
pytest tests/unit/test_goal_processor.py         # Goal decomposition
pytest tests/unit/test_tool_discovery.py        # Tool selection
pytest tests/integration/test_agent_execution.py # End-to-end workflows
pytest tests/performance/test_agent_response.py  # Performance benchmarks
```

## 🔮 Future Usage Examples

### Goal-Driven Agent (Planned)

```python
from thales.agents import BaseAgent
from thales.llm import OpenAIClient

# Create agent with goal processing
agent = BaseAgent(
    llm_client=OpenAIClient(api_key="your-key"),
    goal_processor=GoalProcessor(),
    tool_discovery=ToolDiscoveryEngine()
)

# Execute natural language goals
result = await agent.execute_goal(
    "Analyze the project files and create a summary report"
)
```

### Knowledge Graph RAG (Planned)

```python
from thales.rag import RAGAgent
from thales.rag.graph import Neo4jDatabase

# RAG agent with knowledge graph
rag_agent = RAGAgent(
    graph_db=Neo4jDatabase("bolt://localhost:7687"),
    vector_store=ChromaDB("./data/vectors")
)

# Retrieve contextual information
context = await rag_agent.retrieve_context(
    "What are the best practices for agent memory systems?"
)
```

### Multi-Agent Coordination (Planned)

```python
from thales.agents.coordination import WorkflowCoordinator

# Coordinate multiple specialized agents
coordinator = WorkflowCoordinator({
    "researcher": ResearchAgent(),
    "writer": WritingAgent(),
    "reviewer": ReviewAgent()
})

# Execute complex workflows
result = await coordinator.execute_workflow(
    "Research AI agents, write a report, and review for accuracy"
)
```

## 🛠️ Development Setup

### Environment Setup

```bash
# Development dependencies (planned)
pip install -e ".[dev]"

# Code quality tools
black src/                    # Code formatting
mypy src/                     # Type checking
flake8 src/                   # Linting
pytest tests/                 # Testing
```

### Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the development patterns** established in the MCP foundation
4. **Add comprehensive tests** for new functionality
5. **Update documentation** including memory bank files
6. **Submit a pull request**

### Development Principles

- **Progressive Complexity**: Start simple, build incrementally
- **Test-Driven Development**: Write tests first, then implementation
- **Documentation-First**: Document architecture before coding
- **Memory Bank Approach**: Continuous documentation of decisions and learnings

## 📊 Current Status

### What's Working (Production Ready)
- **MCP Client**: Multi-server connection management ✅
- **Configuration**: Type-safe server configuration ✅
- **Tool Execution**: Math and filesystem operations ✅
- **Testing**: Comprehensive integration tests ✅
- **Cline Integration**: Immediate filesystem access ✅

### Minor Issues (In Progress)
- **Asyncio Cleanup**: Cosmetic subprocess cleanup warnings on Windows
- **Interface Consistency**: Minor method naming standardization needed

### Next Milestones
1. **Complete MCP Foundation**: Fix remaining cleanup issues
2. **Agent Framework Design**: Architecture planning and design
3. **Goal Processing**: Natural language goal interpretation
4. **Tool Discovery**: Dynamic MCP server/tool selection

## 🎓 Learning Outcomes

### Technical Skills Developed
- **MCP Protocol**: Deep understanding of client-server architecture
- **Async Python**: Advanced asyncio patterns and resource management
- **Configuration Management**: Type-safe, extensible configuration systems
- **Testing Strategies**: Integration testing for complex systems
- **Agent Patterns**: Foundation for advanced agent development

### Best Practices Demonstrated
- **Modular Architecture**: Pluggable components and clear separation
- **Progressive Development**: Incremental complexity building
- **Documentation-Driven**: Memory bank approach for continuity
- **Production Quality**: Error handling, logging, and testing

## 🔗 Resources

### Documentation
- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP documentation
- [Memory Bank](./memory-bank/) - Project planning and architecture docs
- [System Patterns](./memory-bank/systemPatterns.md) - Architecture patterns and decisions

### Dependencies
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Official MCP client library
- [AsyncIO](https://docs.python.org/3/library/asyncio.html) - Asynchronous I/O framework

### Future Integrations (Planned)
- [OpenAI API](https://platform.openai.com/) - LLM provider integration
- [Anthropic Claude](https://www.anthropic.com/) - Alternative LLM provider
- [Neo4j](https://neo4j.com/) - Graph database for knowledge graphs
- [ChromaDB](https://www.trychroma.com/) - Vector database for embeddings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- **Model Context Protocol** team for the excellent protocol and SDK
- **Cline** for providing the initial MCP integration inspiration
- **Open source community** for the tools and libraries that make this possible

---

**Ready to learn AI agents by building them?** Start with the MCP foundation and evolve toward a comprehensive agent framework. Each phase builds practical skills while creating reusable components for future projects.

*This project transforms agent development from a complex, fragmented learning experience into a structured, practical journey that produces both deep understanding and production-ready capabilities.*
