from abc import ABC, abstractmethod


class BaseGithubAdapter(ABC):
    @abstractmethod
    def get_subnet_roadmap(self, subnet_id: int) -> str:
        pass

