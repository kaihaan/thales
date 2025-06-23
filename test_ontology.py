"""
Comprehensive test suite for Agent Ontology system
"""

import unittest
from datetime import datetime, timedelta

from thales.agents import (
    AgentOntology, AgentIdentity, AgentType, CommunicationStyle,
    Goal, GoalType, GoalStatus, TimeConstraint,
    Task, TaskType, TaskStatus
)

class TestAgentOntology(unittest.TestCase):
    """Test cases for Agent Ontology system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.identity = AgentIdentity(
            agent_id="test_agent",
            name="TestAgent",
            agent_type=AgentType.GENERAL,
            domain_expertise=["testing", "mathematics"]
        )
        self.ontology = AgentOntology(identity=self.identity)
    
    def test_agent_identity_creation(self):
        """Test agent identity creation"""
        self.assertEqual(self.identity.name, "TestAgent")
        self.assertEqual(self.identity.agent_type, AgentType.GENERAL)
        self.assertIn("testing", self.identity.domain_expertise)
        self.assertIsInstance(self.identity.personality_traits, dict)
    
    def test_goal_creation_and_management(self):
        """Test goal creation and management"""
        goal = Goal( 
            goal_id="test_goal",
            description="Test goal",
            goal_type=GoalType.ACHIEVEMENT,
            priority=1
        )
        
        # Test goal creation
        self.assertEqual(goal.goal_id, "test_goal")
        self.assertEqual(goal.status, GoalStatus.PENDING)
        self.assertEqual(goal.progress, 0.0)
        
        # Test adding goal to ontology
        self.ontology.add_goal(goal)
        self.assertIn(goal, self.ontology.current_goals)
        
        # Test goal progress
        goal.update_progress(0.5, "Halfway done")
        self.assertEqual(goal.progress, 0.5)
        
        # Test goal completion
        goal.update_progress(1.0, "Completed")
        self.assertEqual(goal.status, GoalStatus.COMPLETED)
    
    def test_task_creation_and_execution(self):
        """Test task creation and execution"""
        task = Task(
            task_id="test_task",
            action="test_action",
            task_type=TaskType.EXECUTION,
            description="Test task"
        )
        
        # Test task creation
        self.assertEqual(task.task_id, "test_task")
        self.assertEqual(task.status, TaskStatus.PENDING)
        
        # Test task execution lifecycle
        task.start_execution()
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertIsNotNone(task.started_at)
        
        # Test task completion
        task.complete_task("Test result", confidence=0.9, quality_score=0.8)
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.result, "Test result")
        self.assertEqual(task.confidence, 0.9)
        self.assertEqual(task.quality_score, 0.8)
    
    def test_goal_feasibility_assessment(self):
        """Test goal feasibility assessment"""
        goal = Goal(
            goal_id="math_goal",
            description="Calculate mathematical expressions",
            resource_requirements=["calculator"]
        )
        
        feasibility = self.ontology.assess_goal_feasibility(goal)
        self.assertIsInstance(feasibility, float)
        self.assertGreaterEqual(feasibility, 0.0)
        self.assertLessEqual(feasibility, 1.0)
    
    def test_goal_execution_planning(self):
        """Test goal execution planning"""
        goal = Goal(
            goal_id="planning_test",
            description="Test planning",
            goal_type=GoalType.ACHIEVEMENT
        )
        
        tasks = self.ontology.plan_goal_execution(goal)
        self.assertIsInstance(tasks, list)
        self.assertGreater(len(tasks), 0)
        
        # Check task relationships
        for task in tasks:
            self.assertEqual(task.parent_goal, goal.goal_id)
            self.assertIsInstance(task.task_type, TaskType)
    
    def test_action_validation(self):
        """Test action validation"""
        # Test allowed action
        self.assertTrue(self.ontology.validate_action("calculate", {}))
        
        # Test action with constraints
        self.identity.operating_constraints = ["no_delete"]
        self.assertFalse(self.ontology.validate_action("delete_file", {}))
    
    def test_ontology_summary(self):
        """Test ontology summary generation"""
        summary = self.ontology.get_ontology_summary()
        
        self.assertIn("identity", summary)
        self.assertIn("goals", summary)
        self.assertIn("tasks", summary)
        self.assertIn("last_updated", summary)
        
        self.assertEqual(summary["identity"]["name"], "TestAgent")

if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
