"""
test script for EnhancedMCPClient
"""

from thales.mcp.server import MCPServerManager, MCPServerConfig

def test_config_manager() -> None:
    """ Test MCPServerManager """
    print("🧪 Testing MCP Configuration Manager")
    print("=" * 50)

    # init config manager
    config_manager = MCPServerManager()

    # Test 1: List available servers
    print("\n📋 Available Servers:")
    servers = config_manager.list_configured_servers()
    for name, config in servers.items():
        print(f"  ✅ {name}: {config.description}")
        print(f"     Command: {config.command}")
        print(f"     Args: {config.args}")

    # Test 2: Get specific server configurations
    print("\n🔍 Testing Server Retrieval:")
    try:
        filesystem_config = config_manager.get_server("filesystem")
        print(f"  ✅ Filesystem server: {filesystem_config.description}")
        print(f"     Command: {filesystem_config.command} {' '.join(filesystem_config.args)}")
        
        math_config = config_manager.get_server("local-math")
        print(f"  ✅ Math server: {math_config.description}")
        print(f"     Command: {math_config.command} {' '.join(math_config.args)}")
        
    except Exception as e:
        print(f"  ❌ Error retrieving server: {e}")

    # Test 3: Test error handling for unknown server
    print("\n⚠️  Testing Error Handling:")
    try:
        unknown_config = config_manager.get_server("nonexistent-server")
        print("  ❌ Should have thrown an error!")
    except ValueError as e:
        print(f"  ✅ Correctly caught error: {e}")

    # Test 4: Test adding a new server
    print("\n➕ Testing Adding New Server:")
    new_server = MCPServerConfig(
        name="test-server",
        command="echo",
        args=["Hello from test server"],
        description="A test server for validation"
    )

    config_manager.add_server(new_server)
    
    try:
        retrieved = config_manager.get_server("test-server")
        print(f"  ✅ Successfully added and retrieved: {retrieved.description}")
    except Exception as e:
        print(f"  ❌ Error with new server: {e}")
    
    print("\n🎉 Configuration testing complete!")

    # test execution of maths tools
    

if __name__ == "__main__":
    test_config_manager()