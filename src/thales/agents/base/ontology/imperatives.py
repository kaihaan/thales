""" "
Class abstract for AI Agnt Imeratives
- Interactive: Bool - whether the AI needs to keep Human in the loop
- Reflective: Bool - whether the AI needs to reflect on its actions

- RefectionRules: List[Rule]
"""

from uuid import UUID, uuid4

# class Animal(ABC):
#     @abstractmethod
#     def speak(self):
#         pass


class ReflectionRule:
    """instructs AI what to reflect on
    tags to assist with autonomous searching"""

    id: UUID
    tags: list[str] | None
    usedfor: str
    rule: str

    def __init__(
        self,
        *,
        rule: str,
        tags: list[str] | None,
        usedfor: str,
    ) -> None:
        self.id = uuid4()
        self.rule = rule
        self.tags = tags
        self.usedfor = usedfor


class Imperatives:
    """defines imperative instructions for an AI Agent
    tags to assist with autonomous searching"""

    id: UUID
    description: str
    tags: list[str] | None
    interactive: bool = False
    reflections: None | list[ReflectionRule] = None

    def __init__(
        self,
        *,
        description: str,
        tags: list[str] | None,
        interactive: bool = False,
        reflections: list[ReflectionRule],
    ) -> None:
        self.id = uuid4()
        self.description = description
        self.tags = tags
        self.interactive = interactive
        self.reflections = reflections
