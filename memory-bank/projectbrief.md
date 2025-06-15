# Project Brief: Modular AI Agent Learning Project

## Core Objective

Learn about AI Agents, python package development, MCP Servers, MCP clients and Knowledge Graph based RAG Agents by creating a modular Agent Framework.

## Primary Goals

### 1. Education - learn by doing

- **Cline Coding**: Learn Cline coding best practices
- **Python Package Development**: Learn how to create and deploy high quality Python Packages
- **MCP Framework**: Understand MCP through both consumption and creation
- **Agent RAG using Knowledge Graph**: How RAG performance can be improved using Knowledge Graphs and AI Agents
- **Agent Design Patterns**: enable best-practice Agent design patterns through the Framework 
- **Multi-Agent Design Patterns**: enable best-practice Multi-Agent design patterns through the Framework 
- **AI Agent Memory**: short term and longer-term semantic memory 

### 2. Create a reusable python package for future projects

- A flexible, robust and modern AI Agent package
- Allows use of most suitable LLM for the task
- Takes Goals as an input
- Discovers relevant tools by searching available MCP servers
- Uses AI Agent as Tool to pull relevant context from Knowledge Graph based RAG
- Maintains effective memories in suitable databases

### 3. Develop good coding habits

- Robust planning and design
- Incremental development, starting with simple elements and iteratively adding features
- Good documentation
- Unit and integration testing
- Test driven development
- Effective use if AI coding tools (Cline)

## Implementation Strategy

### Phase 1: Reference Implementation (Completed)

- Configure Cline MCP settings for immediate filesystem access
- Establish working reference for comparison and debugging

### Phase 2: Configuration System (Completed)

- Create centralized MCP server configuration management
- Implement `MCPConfigManager` with dataclass patterns
- Support multiple server types (NPX, Python, future HTTP)

### Phase 3: Enhanced Client (In Progress)

- Build production-ready MCP client
- Implement connection lifecycle management
- Add interactive testing capabilities

### Phase 4: Testing & Validation (Current Focus)

- Comprehensive tool execution tests
- Multi-server integration validation
- Performance and reliability testing

### Phase 5: Documentation & Extension (Planned)

- Usage documentation and examples
- Additional server integrations
- Advanced client features


## Technical Constraints

- **Security**: Filesystem access limited to project directory
- **Platform**: Windows development environment with asyncio considerations
- **Dependencies**: Official MCP Python SDK, minimal external requirements
- **Architecture**: Modular design supporting future server additions

## Educational Value

This project teaches:

- MCP protocol fundamentals
- Async Python programming patterns
- Configuration management systems
- Test-driven development
- Client-server architecture
- Tool integration patterns
