# src/thales/rag/search/agent.py

from typing import Any, List, Optional
import asyncio

from thales.agents.base import BaseAgent, TaskResult, AgentOntology, Task
from thales.rag.data.models import Context, SearchResult
from thales.rag.vector.base import VectorStore
from thales.rag.graph.base import GraphDatabase

class RAGAgent(BaseAgent):
    """A specialized agent for retrieving context from a knowledge graph."""

    def __init__(
        self,
        vector_store: VectorStore,
        graph_db: GraphDatabase,
        ontology: AgentOntology,
        **kwargs: Any
    ):
        """
        Initializes the RAGAgent.
        
        Args:
            vector_store: An instance of a VectorStore implementation.
            graph_db: An instance of a GraphDatabase implementation.
            ontology: The agent's ontology.
            **kwargs: Arguments passed to the BaseAgent.
        """
        super().__init__(ontology=ontology, **kwargs)
        self.vector_store = vector_store
        self.graph_db = graph_db

    async def retrieve_context(
        self,
        query: str,
        k: int = 5,
        depth: int = 1,
        tags: Optional[List[str]] = None
    ) -> List[Context]:
        """
        The primary method for this agent. It retrieves and ranks context.
        """
        print(f"RAGAgent: Retrieving context for query: '{query}' with tags: {tags}")
        initial = self.vector_store.similarity_search_sync(query, k=k, metadata=None)
        vector_items: List[SearchResult] = []
        for ids_group, docs_group, metas_group, dists_group in zip(
            initial.ids,
            initial.documents or [],
            initial.metadatas or [],
            initial.distances or []
        ):
            vector_items.append(
                SearchResult(
                    ids=[ids_group],
                    documents=[docs_group] if docs_group is not None else None,
                    metadatas=[metas_group] if metas_group is not None else None,
                    distances=[dists_group] if dists_group is not None else None
                )
            )
        node_ids = [id for group in initial.ids for id in group]
        connected_nodes = await self.graph_db.get_connected_nodes(node_ids, depth=depth, tags=tags)
        final_context = self._rank_and_combine(vector_items, connected_nodes)
        print(f"RAGAgent: Found {len(final_context)} context items.")
        return final_context

    def _rank_and_combine(self, vector_results: List[SearchResult], graph_results: List[SearchResult]) -> List[Context]:
        """
        Dummy ranking logic. Creates a context object for each initial vector result.
        """
        contexts = []
        for vec_res in vector_results:
            original_id = vec_res.ids[0][0]
            related = [
                gr for gr in graph_results
                if gr.metadatas and gr.metadatas[0][0].get("original_node") == original_id
            ]
            score = vec_res.distances[0][0] if vec_res.distances else 0.0
            ctx = Context(
                source_node=vec_res,
                related_nodes=related,
                combined_relevance=score
            )
            contexts.append(ctx)
        return contexts

    async def execute_task(self, task: Task) -> TaskResult:
        """
        Overrides the BaseAgent's execute_task to handle retrieval tasks.
        """
        print(f"RAGAgent executing task: {task.action}")
        if task.action == "retrieve_context":
            query = task.description
            if query:
                context = await self.retrieve_context(query)
                return TaskResult(task_id=task.task_id, success=True, result=context, tool_used="RAGAgent/retrieve_context")
            else:
                return TaskResult(task_id=task.task_id, success=False, result=None, error="No query provided in task description")

        return await super().execute_task(task)
