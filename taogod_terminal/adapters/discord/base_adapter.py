from abc import ABC, abstractmethod
from typing import Dict, List

from taogod_terminal.adapters.discord_adapter import MessageData


class BaseDiscordAdapter(ABC):
    async def reload_data(self) -> None:
        pass

    @abstractmethod
    def get_subnet_messages(self, subnet_id: int) -> str:
        pass

    @abstractmethod
    def get_subnet_message_map(self) -> Dict[int, List[MessageData]]:
        pass
