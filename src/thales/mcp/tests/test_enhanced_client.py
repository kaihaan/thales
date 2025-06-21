"""Test script for executing MCP tools using the EnhancedMCPClient"""
import asyncio
import sys
import os
from thales.utils.logger.logger import logger

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from client.client import EnhancedMCPClient

class MCPToolTester:
    def __init__(self):
        self.client = EnhancedMCPClient()

    async def test_math_operations(self):
        """Test math server operations using EnhancedMCPClient"""
        print("\n🧮 Testing Math Server Operations")
        print("=" * 50)

        try:
            # Connect to math server
            await self.client.connect("local-math")

            # Test basic arithmetic operations
            math_tests = [
                ("add", {"a": 5, "b": 3}, "5 + 3"),
                ("subtract", {"a": 10, "b": 4}, "10 - 4"),
                ("multiply", {"a": 6, "b": 7}, "6 × 7"),
                ("divide", {"a": 15, "b": 3}, "15 ÷ 3"),
                ("power", {"a": 2, "b": 8}, "2^8"),
                ("sqrt", {"a": 16}, "√16"),
                ("factorial", {"a": 5}, "5!"),
            ]

            for tool_name, args, description in math_tests:
                try:
                    print(f"\n🔧 Testing {tool_name}: {description}")
                    result = await self.client.execute_tool("local-math", tool_name, args)
                    
                    # Extract result content
                    if hasattr(result, 'content') and result.content:
                        result_text = result.content[0].text
                    else:
                        result_text = str(result)
                    
                    print(f"  ✅ Result: {result_text}")
                    
                except Exception as e:
                    print(f"  ❌ Error with {tool_name}: {e}")

        except Exception as e:
            print(f"❌ Math server test failed: {e}")

    async def test_filesystem_operations(self):
        """Test filesystem server operations using EnhancedMCPClient"""
        print("\n📁 Testing Filesystem Server Operations")
        print("=" * 50)

        try:
            # Connect to filesystem server
            await self.client.connect("filesystem")
            cwd = os.getcwd()
            logger.debug(f"Tool test script, CWD {cwd}")
            # run as package... CWD = D:\dev\Coursera\Agents\thales\src

            # Test 1: List current directory
            print("\n🔧 Testing list_directory: Current directory")
            try:
                result = await self.client.execute_tool("filesystem", "list_directory", {"path": "."})
                result_text = result.content[0].text if hasattr(result, 'content') else str(result)
                print(f"  ✅ Directory contents: {result_text[:200]}...")
            except Exception as e:
                print(f"  ❌ Error: {e}")

            # Test 2: Create a test file
            test_content = "Hello from MCP filesystem test!\nThis file was created by the test script."
            test_filename = "mcp_test_file.txt"
            
            print(f"\n🔧 Testing write_file: Creating {test_filename}")
            try:
                result = await self.client.execute_tool("filesystem", "write_file", {
                    "path": test_filename,
                    "content": test_content
                })
                result_text = result.content[0].text if hasattr(result, 'content') else str(result)
                print(f"  ✅ File created: {result_text}")
            except Exception as e:
                print(f"  ❌ Error: {e}")

            # Test 3: Read the test file back
            print(f"\n🔧 Testing read_file: Reading {test_filename}")
            try:
                result = await self.client.execute_tool("filesystem", "read_file", {"path": test_filename})
                content = result.content[0].text if hasattr(result, 'content') else str(result)
                print(f"  ✅ File content: {content[:100]}...")
                
                # Verify content matches
                if test_content in content:
                    print("  ✅ Content verification: PASSED")
                else:
                    print("  ❌ Content verification: FAILED")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")

            # Test 4: Get file info
            print(f"\n🔧 Testing get_file_info: Info for {test_filename}")
            try:
                result = await self.client.execute_tool("filesystem", "get_file_info", {"path": test_filename})
                result_text = result.content[0].text if hasattr(result, 'content') else str(result)
                print(f"  ✅ File info: {result_text}")
            except Exception as e:
                print(f"  ❌ Error: {e}")

            # Test 5: Search for files
            print("\n🔧 Testing search_files: Looking for .py files")
            try:
                result = await self.client.execute_tool("filesystem", "search_files", {
                    "path": ".",
                    "pattern": "*.py"
                })
                result_text = result.content[0].text if hasattr(result, 'content') else str(result)
                print(f"  ✅ Found Python files: {result_text[:200]}...")
            except Exception as e:
                print(f"  ❌ Error: {e}")

        except Exception as e:
            print(f"❌ Filesystem server test failed: {e}")

    async def test_client_features(self):
        """Test EnhancedMCPClient specific features"""
        print("\n🔧 Testing EnhancedMCPClient Features")
        print("=" * 50)

        # # Test listing connected servers
        # print("\n📋 Testing list_connected_servers:")
        # await self.client.list_connected_servers()

        # Test server management
        print("\n🔗 Testing server management:")
        
        # Show available servers
        print("Available servers:")
        for name, config in self.client.config_manager.list_connected_servers().items():
            status = "🟢 Connected" if name in self.client.sessions else "⚪ Available"
            print(f"  {status} {name}: {config.description}")


    async def cleanup(self):
        """Clean up using EnhancedMCPClient"""
        print("\n🧹 Cleaning up...")
        
        # Try to delete test file if filesystem server is connected
        if "filesystem" in self.client.sessions:
            try:
                # Check available tools first
                session = self.client.sessions["filesystem"]
                tools_response = await session.list_tools()
                tools = [tool.name for tool in tools_response.tools]
                
                if "delete_file" in tools:
                    await self.client.execute_tool("filesystem", "delete_file", {"path": "mcp_test_file.txt"})
                    print("  ✅ Test file deleted")
                else:
                    print("  ⚠️  Delete tool not available, test file remains")
            except Exception as e:
                print(f"  ⚠️  Could not delete test file: {e}")

         # 2. Explicitly disconnect servers one by one
        for server_name in list(self.client.sessions.keys()):
            try:
                await self.client.disconnect(server_name)
                print(f"  ✅ Disconnected {server_name}")
            except Exception as e:
                print(f"  ⚠️  Error disconnecting {server_name}: {e}")

        # 3. Wait a moment for cleanup
        await asyncio.sleep(0.1)

        # 4. Final cleanup
        await self.client.cleanup()
        print("  ✅ Client connections closed")






async def run_comprehensive_test():
    """Run all MCP tool tests using EnhancedMCPClient"""
    print("🚀 MCP Tool Execution Test Suite (Using EnhancedMCPClient)")
    print("=" * 70)
    
    tester = MCPToolTester()
    
    try:
        # Test math operations
        await tester.test_math_operations()
        
        # Test filesystem operations
        await tester.test_filesystem_operations()
        
        # Test client-specific features
        await tester.test_client_features()
        
        print("\n🎉 All tests completed successcd fully!")
        
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())