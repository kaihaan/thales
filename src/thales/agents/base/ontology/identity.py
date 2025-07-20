from dataclasses import dataclass, field
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

class CommunicationStyle(Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    TECHNICAL = "technical"
    COLLABORATIVE = "collaborative"
    DIRECT = "direct"
    EXPLANATORY = "explanatory"

class DecisionStyle(Enum):
    ANALYTICAL = "analytical"
    INTUITIVE = "intuitive"
    CONSENSUS = "consensus"
    DIRECTIVE = "directive"
    CAUTIOUS = "cautious"
    BOLD = "bold"

@dataclass
class AgentIdentity:
    """Core identity and characteristics of an agent"""
    agent_id: str
    name: str
    agent_type: AgentType
    version: str = "1.0.0"
    description: str = ""
    creator: str = "system"
    created_at: datetime = field(default_factory=datetime.now)
    
    # Personality and behavior traits (0.0 to 1.0)
    personality_traits: Dict[str, float] = field(default_factory=lambda: {
        "curiosity": 0.7,
        "caution": 0.5,
        "creativity": 0.6,
        "persistence": 0.8,
        "collaboration": 0.7,
        "precision": 0.8
    })
    
    communication_style: CommunicationStyle = CommunicationStyle.EXPLANATORY
    decision_making_style: DecisionStyle = DecisionStyle.ANALYTICAL
    
    # Specialization
    domain_expertise: List[str] = field(default_factory=list)
    preferred_mcp_servers: List[str] = field(default_factory=list)
    operating_constraints: List[str] = field(default_factory=list)
    
    def get_trait(self, trait_name: str) -> float:
        """Get personality trait value"""
        return self.personality_traits.get(trait_name, 0.5)
    
    def update_trait(self, trait_name: str, value: float) -> None:
        """Update personality trait (0.0 to 1.0)"""
        self.personality_traits[trait_name] = max(0.0, min(1.0, value))