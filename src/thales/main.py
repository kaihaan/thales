'''
Modular AI Agent Framework - Main Entry Point
Phase A: MCP Foundation (COMPLETE)
Phase B: Agent Framework Core (STARTING)
==============================================================
Use this to demonstrate & test the currently working features
'''

import asyncio
from datetime import datetime, timedelta

# Import Agent Framework
from thales.agents import (
    AgentOntology, AgentIdentity, AgentType, CommunicationStyle, DecisionStyle,
    Goal, GoalType, GoalStatus, TimeConstraint,
    Task, TaskType, TaskStatus
)


def make_an_ontology() -> AgentOntology:
    """Create a test agent with ontology"""
    
    # Create agent identity
    identity = AgentIdentity(
        agent_id="test_agent_001",
        name="TestBot",
        agent_type=AgentType.GENERAL,
        version="1.0.0",
        description="A test agent for demonstrating the ontology system",
        creator="thales_framework",
        domain_expertise=["mathematics", "file_operations", "testing"],
        preferred_mcp_servers=["local-math", "filesystem"],
        operating_constraints=["no_network_access", "project_directory_only"]
    )
    
    # Customize personality traits
    identity.personality_traits.update({
        "curiosity": 0.9,
        "caution": 0.7,
        "creativity": 0.6,
        "persistence": 0.8,
        "collaboration": 0.8,
        "precision": 0.9
    })
    
    # Create ontology with the identity
    ontology = AgentOntology(identity=identity)
    
    return ontology

def create_test_goals() -> list[Goal]:
    """Create test goals for the agent"""
    
    goals = []
    
    # Goal 1: Mathematical calculation
    math_goal = Goal(
        goal_id="goal_001",
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
    goals.append(math_goal)
    
    # Goal 2: File operations
    file_goal = Goal(
        goal_id="goal_002", 
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
        dependencies=["goal_001"],  # Depends on math goal
        time_constraints=TimeConstraint(
            estimated_duration=timedelta(minutes=3),
            max_duration=timedelta(minutes=5)
        )
    )
    goals.append(file_goal)
    
    # Goal 3: Exploration goal
    explore_goal = Goal(
        goal_id="goal_003",
        description="Explore available MCP tools and document capabilities",
        goal_type=GoalType.EXPLORATION,
        priority=3,
        urgency=3,
        success_criteria=[
            "List all available MCP servers",
            "Document each server's capabilities",
            "Test basic functionality of each tool"
        ],
        resource_requirements=["local-math", "filesystem"]
    )
    goals.append(explore_goal)
    
    return goals



def test_ontology_system() -> AgentOntology:
    """Test the agent ontology system"""
    
    print("🧠 Testing Agent Ontology System")
    print("=" * 50)
    
    # Create test agent
    ontology = make_an_ontology()
    print(f"✅ Created agent: {ontology.identity.name}")
    print(f"   Type: {ontology.identity.agent_type.value}")
    print(f"   Expertise: {', '.join(ontology.identity.domain_expertise)}")
    print(f"   Personality traits:")
    for trait, value in ontology.identity.personality_traits.items():
        print(f"     {trait}: {value}")
    
    # Create and add goals
    test_goals = create_test_goals()
    print(f"\n📋 Adding {len(test_goals)} test goals:")
    
    for goal in test_goals:
        ontology.add_goal(goal)
        feasibility = ontology.assess_goal_feasibility(goal)
        print(f"   Goal: {goal.description}")
        print(f"     Priority: {goal.priority}, Urgency: {goal.urgency}")
        print(f"     Feasibility: {feasibility:.2f}")
        print(f"     Success criteria: {len(goal.success_criteria)} items")
    
    # Test goal planning
    print(f"\n🎯 Testing goal execution planning:")
    for goal in ontology.current_goals:
        tasks = ontology.plan_goal_execution(goal)
        print(f"   Goal: {goal.goal_id}")
        print(f"     Generated {len(tasks)} tasks:")
        for task in tasks:
            print(f"       - {task.action}: {task.description}")
            ontology.add_task(task)
    
    # Test task management
    print(f"\n📝 Task Management:")
    pending_tasks = ontology.get_pending_tasks()
    print(f"   Pending tasks: {len(pending_tasks)}")
    
    # Simulate task execution
    if pending_tasks:
        first_task = pending_tasks[0]
        print(f"   Simulating execution of: {first_task.action}")
        
        # Start task
        first_task.start_execution()
        print(f"     Status: {first_task.status.value}")
        
        # Complete task
        first_task.complete_task(
            result="Analysis completed successfully",
            confidence=0.9,
            quality_score=0.85
        )
        print(f"     Completed with confidence: {first_task.confidence}")
        print(f"     Quality score: {first_task.quality_score}")
        
        # Move to completed
        ontology.complete_task(first_task.task_id)
    
    # Test action validation
    print(f"\n🔒 Testing action validation:")
    test_actions = [
        "calculate_square_root",
        "create_file", 
        "network_request",  # Should be blocked
        "delete_system_files"  # Should be blocked
    ]
    
    for action in test_actions:
        is_valid = ontology.validate_action(action, {})
        status = "✅ ALLOWED" if is_valid else "❌ BLOCKED"
        print(f"   {action}: {status}")
    
    # Display ontology summary
    print(f"\n📊 Agent Ontology Summary:")
    summary = ontology.get_ontology_summary()
    print(f"   Agent: {summary['identity']['name']} ({summary['identity']['type']})")
    print(f"   Goals: {summary['goals']['active']} active, {summary['goals']['completed']} completed")
    print(f"   Tasks: {summary['tasks']['active']} active, {summary['tasks']['completed']} completed")
    print(f"   Last updated: {summary['last_updated']}")
    
    # Test goal progress tracking
    print(f"\n📈 Testing goal progress tracking:")
    if ontology.current_goals:
        test_goal = ontology.current_goals[0]
        print(f"   Goal: {test_goal.description}")
        print(f"   Initial progress: {test_goal.progress}")
        
        # Update progress
        test_goal.update_progress(0.3, "Started analysis phase")
        print(f"   Progress after analysis: {test_goal.progress}")
        
        test_goal.update_progress(0.7, "Completed calculation")
        print(f"   Progress after calculation: {test_goal.progress}")
        
        test_goal.update_progress(1.0, "Goal completed successfully")
        print(f"   Final progress: {test_goal.progress}")
        print(f"   Status: {test_goal.status.value}")
    
    print(f"\n🎉 Ontology system test completed!")
    return ontology

def main() -> None:
    """Main function - to demonstrate and test currently working functionality """
    print("Thales AI Agent Framework - Phase B")
    print("=" * 60)
    
    # intended usage / syntax
    # Step 0. Operator Browses Agent Context Library on a web interface
    # Step 1. Add or retrieve an AgentOntology to the AgentContext MCP
    #         - ontology = AgentOnology({init})
    #         - await mcp('AgentContext').addOntology(ontology)
    # Step 2. Add or retreive Agent Goals to the AgentContext MCP
    #         - goals = list[ Goal({init}), Goal({init})]
    #         - await mcp('AgentContext').addGoals(goals=goals, name="goal set name")
    # Step 3. Create new agent, retrieving Ontology & Goals from AgentContent MCP
    #         - agent = Agent(ontology="ontology.name", goals = "goal set name", llm="llm")
    # Step 4. Run agent
    #         - output = await agent.start()
    # Step 5. Display final output

    ontology = make_an_ontology()
    # TODO enable MCP client to make state persistent with database


if __name__ == "__main__":
    main()