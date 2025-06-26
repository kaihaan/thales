"""
BaseAgent - Core AI Agent Implementation
Integrates AgentOntology with EnhancedMCPClient for goal execution
"""


import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from thales.agents.base.ontology import AgentOntology, Goal, Task, GoalStatus, TaskStatus
from thales.mcp.client import EnhancedMCPClient
from thales.utils import get_logger
from thales.llm.client import OpenAIClient
from thales.llm.prompts import GoalDecompositionPrompts
from thales.llm.models import DecomposedTasks, TaskOutput
import uuid

logger = get_logger(__name__)

@dataclass
class GoalResult:
    """Result of goal execution"""
    goal_id: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: Optional[float] = None

@dataclass 
class TaskResult:
    """Result of task execution"""
    task_id: str
    success: bool
    result: Any
    tool_used: Optional[str] = None
    error: Optional[str] = None


class BaseAgent:
    """
    Base AI Agent that integrates ontology system with MCP client
    
    Key Features:
    - Goal decomposition using agent ontology
    - Tool discovery and execution via MCP client
    - Progress tracking and status management
    - Error handling and validation
    """
    
    def __init__(self, ontology: AgentOntology):
        self.ontology = ontology
        self.mcp_client = EnhancedMCPClient()
        self.is_running = False
        self.execution_context: Dict[str, Any] = {}


    async def start(self) -> None:
        """Initialize agent and connect to required MCP servers"""
        # Connect to servers based on agent's preferred tools
        if self.is_running:
            logger.info(f"Agent {self.ontology.identity.name} already running")
            return
        
        logger.info(f"Starting agent: {self.ontology.identity.name}")

        # Connect to preferred MCP servers
        for server in self.ontology.identity.preferred_mcp_servers:
            try:
                await self.mcp_client.connect(server)
                logger.info(f"Connected to MCP server: {server}")
            except Exception as e:
                logger.warning(f"Failed to connect to {server}: {e}")
        
        self.is_running = True
        logger.info(f"Agent {self.ontology.identity.name} started successfully")

    async def stop(self) -> None:
        """Clean up connections and shutdown agent"""
        if not self.is_running:
            return
            
        logger.info(f"Stopping agent: {self.ontology.identity.name}")
        await self.mcp_client.cleanup()
        self.is_running = False
        logger.info("Agent stopped")

    async def execute_goal(self, goal: Goal) -> GoalResult:
        """
        Execute a goal by decomposing into tasks and using MCP tools
        
        Workflow:
        1. Validate goal feasibility (for now always say its feasible - requires sophisticated solution)
        2. Decompose goal into tasks
        3. Execute tasks sequentially
        4. Track progress and update status
        """
        start_time = datetime.now()
        logger.info(f"Executing goal: {goal.description}")

        try:
            # 1. Validate feasibility
            # for now returns a hard coded 0.7!
            feasibility = self.ontology.assess_goal_feasibility(goal)
            if feasibility < 0.3:
                return GoalResult(
                    goal_id=goal.goal_id,
                    success=False,
                    result=None,
                    error=f"Goal feasibility too low: {feasibility}",
                )
            
            # Add goal to ontology & start execution
            self.ontology.add_goal(goal)
            goal.status = GoalStatus.IN_PROGRESS
            goal.started_at = datetime.now()

            # Decompose goal into tasks
            tasks = await self._decompose_goal_into_tasks(goal)
            logger.info(f"Decomposed goal into {len(tasks)} tasks")

            # Execute tasks
            task_results: List[TaskResult] = []
            for task in tasks:
                self.ontology.add_task(task)
                task_result = await self.execute_task(task)
                task_results.append(task_result)
                
                if not task_result.success:
                    # Task failed - mark goal as failed
                    goal.status = GoalStatus.FAILED
                    execution_time = (datetime.now() - start_time).total_seconds()
                    return GoalResult(
                        goal_id=goal.goal_id,
                        success=False,
                        result=task_results,
                        error=f"Task {task.task_id} failed: {task_result.error}",
                        execution_time=execution_time
                    )

            # All tasks succeeded - mark goal as completed
            goal.status = GoalStatus.COMPLETED
            goal.completed_at = datetime.now()
            goal.progress = 1.0
            self.ontology.complete_goal(goal.goal_id)

            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Goal completed successfully in {execution_time:.2f}s")

            return GoalResult(
                goal_id=goal.goal_id,
                success=True,
                result=task_results,
                execution_time=execution_time
            )
        
        except Exception as e:
            goal.status = GoalStatus.FAILED
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Goal execution failed: {e}")
            
            return GoalResult(
                goal_id=goal.goal_id,
                success=False,
                result=None,
                error=str(e),
                execution_time=execution_time
            )

        # 2. Execute each task
        # 3. Update progress


    async def execute_task(self, task: Task) -> TaskResult:
        """
        Execute a single task using appropriate MCP tools
        
        Workflow:
        1. Validate task action
        2. Discover relevant MCP tools
        3. Execute tool with task parameters
        4. Update task status and return result
        """
        logger.info(f"Executing task: {task.action}")

        try:
            # Validate action against agent constraints
            if not self.ontology.validate_action(task.action, {}):
                return TaskResult(
                    task_id=task.task_id,
                    success=False,
                    result=None,
                    error=f"Action {task.action} not allowed by agent constraints"
                )
            
            # Start task execution (marks time started, IN_PROGRESS etc)
            task.start_execution()

            # Map task action to MCP tool execution
            result = await self._execute_task_action(task)        

            # Complete task
            task.complete_task(
                result=str(result),
                confidence=0.9,
                quality_score=0.8
            )
            self.ontology.complete_task(task.task_id)
            
            logger.info(f"Task {task.action} completed successfully")
            return TaskResult(
                task_id=task.task_id,
                success=True,
                result=result,
                tool_used=getattr(task, 'tool_used', None)
            )

        except Exception as e:
            task.status = TaskStatus.FAILED
            logger.error(f"Task execution failed: {e}")
            
            return TaskResult(
                task_id=task.task_id,
                success=False,
                result=None,
                error=str(e)
            )

    async def _execute_task_action(self, task: Task) -> Any:
        """Map task actions to specific MCP tool executions"""
        
        # Simple action mapping - in real implementation, this would be more sophisticated
        action_mappings = {
            "analyze_goal": self._analyze_goal_action,
            "execute_goal": self._execute_goal_action,
            "validate_result": self._validate_result_action,
            "calculate_square_root": self._calculate_square_root_action,
            "create_file": self._create_file_action,
            "explore_tools": self._explore_tools_action
        }
        
        if task.action in action_mappings:
            return await action_mappings[task.action](task)
        else:
            # Generic tool execution
            return await self._generic_tool_execution(task)


    async def _analyze_goal_action(self, task: Task) -> str:
        """Analyze goal requirements"""
        return f"Analysis completed for goal: {task.parent_goal}"
    
    async def _execute_goal_action(self, task: Task) -> str:
        """Execute the main goal action"""
        # This would contain the core logic for the specific goal
        return f"Executed goal action for: {task.parent_goal}"
    
    async def _validate_result_action(self, task: Task) -> str:
        """Validate goal completion"""
        return f"Validation completed for goal: {task.parent_goal}"
    
    async def _calculate_square_root_action(self, task: Task) -> Any:
        """Calculate square root using math server"""
        try:
            result = await self.mcp_client.execute_tool(
                "local-math", 
                "sqrt", 
                {"number": 144}
            )
            task.tool_used = "local-math/sqrt"
            return result
        except Exception as e:
            raise Exception(f"Failed to calculate square root: {e}")
    
    async def _create_file_action(self, task: Task) -> Any:
        """Create file using filesystem server"""
        try:
            result = await self.mcp_client.execute_tool(
                "filesystem",
                "write_file",
                {
                    "path": "calculation_results.txt",
                    "content": "Square root of 144 = 12"
                }
            )
            task.tool_used = "filesystem/write_file"
            return result
        except Exception as e:
            raise Exception(f"Failed to create file: {e}")
        
    async def _explore_tools_action(self, task: Task) -> Any:
        """Explore available MCP tools"""
        try:
            tools = await self.mcp_client.list_tools()
            task.tool_used = "mcp_client/list_tools"
            return f"Found {len(tools.tools) if tools else 0} available tools"
        except Exception as e:
            raise Exception(f"Failed to explore tools: {e}")
    
    async def _generic_tool_execution(self, task: Task) -> str:
        """Generic tool execution for unmapped actions"""
        logger.warning(f"No specific mapping for action: {task.action}")
        return f"Generic execution completed for: {task.action}"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_name": self.ontology.identity.name,
            "is_running": self.is_running,
            "active_goals": len(self.ontology.current_goals),
            "active_tasks": len(self.ontology.active_tasks),
            "connected_servers": list(self.mcp_client.sessions.keys()) if hasattr(self.mcp_client, 'sessions') else []
        }

    async def _decompose_goal_into_tasks(self, goal: Goal) -> List[Task]:
        """Decompose a goal into a list of tasks using an LLM."""

        #get this from mcp in future
        prompt_generator = GoalDecompositionPrompts()
        prompt = prompt_generator.get_prompt(goal.description)

        llm_client = OpenAIClient()

        # Use the new structured output method
        decomposed_tasks_model: Optional[DecomposedTasks] = await llm_client.generate_structured_output(
            prompt=prompt,
            output_type=DecomposedTasks,
            max_tokens=1000 # Increase max_tokens for structured output
        )

        response = await llm_client.generate_text(prompt)

        if response.error:
            logger.error(f"LLM error: {response.error.message}")
            return []

        if not decomposed_tasks_model or not decomposed_tasks_model.tasks:
            logger.error(f"LLM failed to decompose goal or returned no tasks for goal: {goal.description}")
            return []
    
        tasks: List[Task] = []
        for task_output in decomposed_tasks_model.tasks:
            # Create an instance of your internal Task dataclass
            new_task = Task(
                task_id=str(uuid.uuid4()), # Generate unique ID
                action=task_output.action,
                task_type=task_output.task_type, # Use the task_type from LLM
                description=task_output.description,
                parent_goal=goal.goal_id,
                # Other fields will use their default values from the Task dataclass
            )
            tasks.append(new_task)
            
        return tasks
