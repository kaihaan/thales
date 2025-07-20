"""
Manual test script for BaseAgent
Run this to interactively test your agent implementation
"""

import asyncio
from datetime import datetime, timedelta

from thales.agents import (
    BaseAgent, AgentOntology, AgentIdentity, AgentType, CommunicationStyle, DecisionStyle,
    Goal, GoalType, GoalStatus, TimeConstraint
)

async def create_test_agent() -> BaseAgent:
    """Create a test agent for manual testing"""
    
    # Create agent identity
    identity = AgentIdentity(
        agent_id="manual_test_agent",
        name="ManualTestBot",
        agent_type=AgentType.GENERAL,
        version="1.0.0",
        description="Manual test agent for BaseAgent validation",
        creator="manual_test",
        domain_expertise=["mathematics", "file_operations", "testing"],
        preferred_mcp_servers=["local-math", "filesystem"],
        operating_constraints=["no_network_access", "project_directory_only"]
    )
    
    # Set personality traits
    identity.personality_traits.update({
        "curiosity": 0.9,
        "caution": 0.7,
        "precision": 0.9
    })
    
    # Create ontology
    ontology = AgentOntology(identity=identity)
    
    # Create and start agent
    agent = BaseAgent(ontology)
    await agent.start()
    
    return agent

async def test_math_goal(agent: BaseAgent) -> None:
    """Test mathematical calculation goal"""
    print("\nTesting Math Goal")
    print("=" * 40)
    
    goal = Goal(
        goal_id="math_test_001",
        description="Calculate the square root of 144 and verify the result",
        goal_type=GoalType.ACHIEVEMENT,
        priority=1,
        urgency=7,
        success_criteria=[
            "Calculate square root of 144",
            "Verify result is correct (12)",
            "Document the calculation process"
        ],
        resource_requirements=["local-math"],
        time_constraints=TimeConstraint(
            estimated_duration=timedelta(minutes=5),
            max_duration=timedelta(minutes=10)
        )
    )
    
    print(f"Goal: {goal.description}")
    print(f"Priority: {goal.priority}, Urgency: {goal.urgency}")
    
    # Test feasibility
    feasibility = agent.ontology.assess_goal_feasibility(goal)
    print(f"Feasibility: {feasibility:.2f}")
    
    # Test task planning
    tasks = agent.ontology.plan_goal_execution(goal)
    print(f"Generated {len(tasks)} tasks:")
    for task in tasks:
        print(f"  - {task.action}: {task.description}")
    
    # TODO: Test goal execution when you complete the execute_goal method
    # result = await agent.execute_goal(goal)
    # print(f"Goal execution result: {result}")

async def test_file_goal(agent: BaseAgent) -> None:
    """Test file operation goal"""
    print("\nTesting File Goal")
    print("=" * 40)
    
    goal = Goal(
        goal_id="file_test_001",
        description="Create a test file with calculation results",
        goal_type=GoalType.ACHIEVEMENT,
        priority=2,
        urgency=5,
        success_criteria=[
            "Create file with calculation results",
            "Verify file was created successfully",
            "Ensure file contains correct data"
        ],
        resource_requirements=["filesystem"],
        time_constraints=TimeConstraint(
            estimated_duration=timedelta(minutes=3),
            max_duration=timedelta(minutes=5)
        )
    )
    
    print(f"Goal: {goal.description}")
    
    # Test task planning
    tasks = agent.ontology.plan_goal_execution(goal)
    print(f"Generated {len(tasks)} tasks:")
    for task in tasks:
        print(f"  - {task.action}: {task.description}")

async def test_agent_status(agent: BaseAgent) -> None:
    """Test agent status reporting"""
    print("\nAgent Status")
    print("=" * 40)
    
    # Test ontology summary
    summary = agent.ontology.get_ontology_summary()
    print(f"Agent: {summary['identity']['name']} ({summary['identity']['type']})")
    print(f"Expertise: {', '.join(summary['identity']['expertise'])}")
    print(f"Goals: {summary['goals']['active']} active, {summary['goals']['completed']} completed")
    print(f"Tasks: {summary['tasks']['active']} active, {summary['tasks']['completed']} completed")
    
    # Test agent status (if you implement get_status method)
    # status = agent.get_status()
    # print(f"Agent running: {status['is_running']}")
    # print(f"Connected servers: {status['connected_servers']}")

async def main() -> None:
    """Main test function"""
    print("🚀 BaseAgent Manual Test Suite")
    print("=" * 50)
    
    agent = await create_test_agent()

    try:
        # Create test agent
        print(f"✅ Created agent: {agent.ontology.identity.name}")
        
        # Run tests
        await test_math_goal(agent)
        await test_file_goal(agent)
        await test_agent_status(agent)
        
        print(f"\n✨ Manual tests completed!")
        print(f"Next steps:")
        print(f"1. Complete the execute_goal() method in BaseAgent")
        print(f"2. Complete the execute_task() method in BaseAgent")
        print(f"3. Add specific task-to-tool mappings")
        print(f"4. Test actual goal execution")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if 'agent' in locals():
            await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
