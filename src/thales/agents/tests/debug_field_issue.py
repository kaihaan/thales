"""
Debug script to test the Field issue fix
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from thales.agents import (
    AgentOntology, AgentIdentity, AgentType,
    Goal, GoalType, GoalStatus, TimeConstraint
)

def test_field_initialization() -> bool:
    """Test that AgentOntology fields are properly initialized"""
    
    print("🔍 Testing AgentOntology field initialization...")
    
    # Create agent identity
    identity = AgentIdentity(
        agent_id="debug_agent",
        name="DebugBot",
        agent_type=AgentType.GENERAL,
        version="1.0.0",
        description="Debug agent for field testing",
        creator="debug_test",
        domain_expertise=["testing"],
        preferred_mcp_servers=["local-math"],
        operating_constraints=["no_network_access"]
    )
    
    print(f"✅ Created identity: {identity.name}")
    
    # Create ontology
    ontology = AgentOntology(identity=identity)
    
    print(f"✅ Created ontology")
    
    # Debug field types
    print(f"\n🔍 Field type analysis:")
    print(f"  current_goals type: {type(ontology.current_goals)}")
    print(f"  current_goals value: {ontology.current_goals}")
    print(f"  active_tasks type: {type(ontology.active_tasks)}")
    print(f"  active_tasks value: {ontology.active_tasks}")
    print(f"  completed_goals type: {type(ontology.completed_goals)}")
    print(f"  completed_tasks type: {type(ontology.completed_tasks)}")
    
    # Test len() operations
    try:
        current_goals_len = len(ontology.current_goals)
        active_tasks_len = len(ontology.active_tasks)
        completed_goals_len = len(ontology.completed_goals)
        completed_tasks_len = len(ontology.completed_tasks)
        
        print(f"\n✅ len() operations successful:")
        print(f"  current_goals length: {current_goals_len}")
        print(f"  active_tasks length: {active_tasks_len}")
        print(f"  completed_goals length: {completed_goals_len}")
        print(f"  completed_tasks length: {completed_tasks_len}")
        
    except Exception as e:
        print(f"❌ len() operation failed: {e}")
        return False
    
    # Test get_ontology_summary
    try:
        summary = ontology.get_ontology_summary()
        print(f"\n✅ get_ontology_summary() successful:")
        print(f"  Agent: {summary['identity']['name']}")
        print(f"  Goals: {summary['goals']['active']} active, {summary['goals']['completed']} completed")
        print(f"  Tasks: {summary['tasks']['active']} active, {summary['tasks']['completed']} completed")
        
    except Exception as e:
        print(f"❌ get_ontology_summary() failed: {e}")
        return False
    
    print(f"\n🎉 All field initialization tests passed!")
    return True

if __name__ == "__main__":
    success = test_field_initialization()
    if success:
        print("\n✅ Field issue has been resolved!")
    else:
        print("\n❌ Field issue still exists!")
