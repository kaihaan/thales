#!/usr/bin/env python3
"""
Simple test to verify the Field issue is fixed
"""

from thales.agents import AgentOntology, AgentIdentity, AgentType

def test_field_fix() -> bool:
    """Test that the Field issue is resolved"""
    print("Testing Field issue fix...")
    
    # Create identity
    identity = AgentIdentity(
        agent_id="test_agent",
        name="TestBot", 
        agent_type=AgentType.GENERAL,
        domain_expertise=["testing"],
        preferred_mcp_servers=["local-math"]
    )
    
    # Create ontology
    ontology = AgentOntology(identity=identity)
    
    # Test field types
    print(f"current_goals type: {type(ontology.current_goals)}")
    print(f"current_goals is list: {isinstance(ontology.current_goals, list)}")
    
    # Test len() operation
    try:
        goals_len = len(ontology.current_goals)
        print(f"current_goals length: {goals_len}")
        print("✅ len() operation successful!")
    except Exception as e:
        print(f"❌ len() operation failed: {e}")
        return False
    
    # Test get_ontology_summary
    try:
        summary = ontology.get_ontology_summary()
        print(f"✅ get_ontology_summary() successful!")
        print(f"   Goals: {summary['goals']['active']} active")
        return True
    except Exception as e:
        print(f"❌ get_ontology_summary() failed: {e}")
        return False

if __name__ == "__main__":
    success = test_field_fix()
    if success:
        print("\n🎉 Field issue has been RESOLVED!")
    else:
        print("\n❌ Field issue still exists!")
