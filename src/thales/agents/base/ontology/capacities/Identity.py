from dataclasses import dataclass, field
import uuid
from enum import Enum
from typing import Dict, List
from datetime import datetime

class AgentType(Enum):
    GENERAL = "general"
    RAG = "rag"
    CODE = "code"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    COORDINATOR = "coordinator"


@dataclass
class Identity:
    """Core identity and characteristics of an agent"""
    name: str
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "1.0.0"
    description: str = ""
    creator: str = "system"
    agent_type: AgentType = AgentType.GENERAL
    created_at: datetime = field(default_factory=datetime.now)