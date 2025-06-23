# Thales: AI Agent Learning Project

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.9.3-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A hands-on learning project for understanding AI agents through building with the Model Context Protocol (MCP).

## What This Project Is

**Thales** is an educational project that teaches AI agent development by starting with a solid MCP foundation and gradually building toward more advanced agent capabilities. The focus is on learning by doing, with each component built to understand the underlying concepts.

## Current Achievements

### ✅ MCP Foundation (Complete)
- **Custom MCP Client**: Multi-server connection management with async resource handling
- **Cline Integration**: Immediate filesystem and math operations through Cline interface
- **Configuration System**: Type-safe server configuration with centralized management
- **Comprehensive Testing**: Validated tool execution across filesystem and math operations
- **Production Ready**: Proper error handling, logging, and resource cleanup

### ✅ Agent Framework (In Progress)
- **Base Agent Structure**: Core agent classes with goal/task management
- **Agent Ontology**: Identity, capabilities, and behavior framework
- **Goal Processing**: Basic goal execution and task decomposition

## Longer-term Vision

The project aims to evolve into a modular agent framework supporting:

- **Goal-Driven Agents**: Natural language goals converted to actionable tasks
- **Dynamic Tool Discovery**: Automatic selection of relevant MCP servers and tools
- **Knowledge Graph RAG**: Enhanced context retrieval using graph relationships
- **Multi-Agent Coordination**: Collaborative agent workflows
- **Educational Package**: Reusable components for learning and future projects

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js (for NPX-based MCP servers)

### Installation
```bash
git clone <repository-url>
cd thales
python -m venv env
env\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Try It Now
```bash
cd src

# Test the MCP client
python -m thales.mcp.client.client local-math

# Run comprehensive tests
python -m thales.mcp.tests.test_enhanced_client
```

## Project Structure

```
thales/
├── memory-bank/          # Project documentation and planning
├── src/thales/
│   ├── mcp/             # MCP Foundation (Complete)
│   │   ├── client/      # Enhanced MCP client
│   │   ├── server/      # Server configurations
│   │   └── tests/       # Test suite
│   ├── agents/          # Agent Framework (In Progress)
│   │   └── base/        # Base agent classes
│   └── utils/           # Shared utilities
└── requirements.txt
```

## Current Status

**Phase A (MCP Foundation)**: ✅ Complete - Production-ready MCP client with comprehensive testing

**Phase B (Agent Framework)**: 🔧 In Progress - Basic agent structure implemented, goal processing underway

**Phase C (Advanced Features)**: 📋 Planned - Knowledge graph RAG, multi-agent patterns

## Contributing

This is primarily an educational project, but contributions that enhance the learning experience are welcome. Please maintain the focus on clear, understandable implementations over complex optimizations.

## Resources

- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP documentation
- [Memory Bank](./memory-bank/) - Project planning and architecture documentation

## License

MIT License - see [LICENSE](LICENSE) file for details.

---
