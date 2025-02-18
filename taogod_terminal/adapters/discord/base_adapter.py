from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class UserData:
    email: str
    global_name: str  # username
    id: str
    username: str

@dataclass
class ChannelData:
    name: str
    type: int  # idk

@dataclass
class MessageData:
    author_name: str
    channel_name: str
    content: str
    timestamp: str

@dataclass
class DMData:
    content: str
    author_name: str
    timestamp: str

@dataclass
class GuildData:
    guild_name: str
    channels: List[ChannelData]
    channel_name_to_messages: Dict[str, List[MessageData]]

@dataclass
class DiscordData:
    user_data: UserData
    dms: List[DMData]  # unused
    guilds: List[GuildData]


class BaseDiscordAdapter(ABC):
    async def reload_data(self) -> None:
        pass

    @abstractmethod
    def get_subnet_messages(self, subnet_id: int) -> str:
        pass

    @abstractmethod
    def get_subnet_message_map(self) -> Dict[int, List[MessageData]]:
        pass
