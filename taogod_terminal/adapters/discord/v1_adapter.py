import asyncio
import json
import logging
import os
import random
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import List, Set, Dict, Optional

import aiohttp
from dotenv import load_dotenv
from taogod_terminal.helpers import convert_to_obj, dict_to_dataclass_or_basemodel
from taogod_terminal.adapters.discord.base_adapter import BaseDiscordAdapter
from taogod_terminal.adapters.discord.base_adapter import UserData, MessageData, DMData, GuildData, \
    DiscordData, ChannelData

logger = logging.getLogger(__name__)


load_dotenv()

FETCH_INTERVAL = timedelta(days=1)
SUBNET_CHANNEL_MAP = {
    "1": "1161764867166961704",
    "2": "1220504695404236800",
    "19": "1186691482749505627",
    "21": "1240801129177157692",
    "24": "1214246819886931988",
    "36": "1301269318213828699",
    "39": "1241046233800507482",
    "43": "1263507367405031434",
    "45": "1267511824601976935"
}

DISCORD_USER_TOKEN = os.environ["DISCORD_USER_TOKEN"]
DISCORD_USER_ID = os.environ["DISCORD_USER_ID"]

OUTPUT_FILE = "fetch_discord_info_results.json"


class DiscordAPI:
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.base_url = "https://discord.com/api/v10"
        self.base_url_v9 = "https://discord.com/api/v9"
        self.headers = {
            "Authorization": f"{self.token}",
            # "User-Agent": "DiscordBot (https://discord.com) Python/3.9 aiohttp/3.8.1"  # Added User-Agent
        }
        self.inaccessible_channels = set()
        self.session = None
        self.semaphore = asyncio.Semaphore(30)  # Reduced concurrent requests
        self.message_cache = defaultdict(list)
        self.global_rate_limit = asyncio.Event()
        self.global_rate_limit.set()
        self.retry_count = 0
        self.max_retries = 3
        self.fetch_interval = FETCH_INTERVAL
        self.channel_scores = {}  # Add this line to store channel scores

    @staticmethod
    def _timestamp_to_snowflake(timestamp):
        """Convert timestamp to Discord snowflake ID"""
        discord_epoch = 1420070400000
        unix_ts = int(timestamp.timestamp() * 1000)
        return (unix_ts - discord_epoch) << 22

    async def connect(self):
        """Initialize persistent aiohttp session and load inaccessible channels"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)  # 30 second timeout
            self.session = aiohttp.ClientSession(timeout=timeout)

            # Load inaccessible channels from users.json
            self.inaccessible_channels: Set[str] = set()

        return self

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def _handle_rate_limit(self, response):
        """Handle rate limiting with exponential backoff"""
        if response.status == 429:
            data = await response.json()
            retry_after = data.get('retry_after', 1)

            # If it's a global rate limit
            if data.get('global', False):
                self.global_rate_limit.clear()
                await asyncio.sleep(retry_after)
                self.global_rate_limit.set()
            else:
                # Add jitter to prevent thundering herd
                jitter = random.uniform(0, 0.1)
                await asyncio.sleep(retry_after + jitter)

            return True
        return False

    async def _make_request(self, endpoint, params=None):
        """Enhanced request handler with better rate limit handling"""
        await self.global_rate_limit.wait()  # Wait for global rate limit to clear

        async with self.semaphore:
            # First try with v10
            for attempt in range(3):
                try:
                    if not self.session:
                        await self.connect()

                    async with self.session.get(
                            f"{self.base_url}{endpoint}",
                            headers=self.headers,
                            params=params
                    ) as response:
                        if response.status == 429:  # Rate limit
                            data = await response.json()
                            retry_after = data.get('retry_after', 10)

                            if data.get('global', False):
                                self.global_rate_limit.clear()
                                await asyncio.sleep(retry_after)
                                self.global_rate_limit.set()
                            else:
                                await asyncio.sleep(retry_after)
                            continue

                        if response.status == 403:
                            if 'channels' in endpoint:
                                channel_id = endpoint.split('/channels/')[1].split('/')[0]
                                self.inaccessible_channels.add(channel_id)
                            return []

                        response.raise_for_status()
                        return await response.json()

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logger.info(f"v10 Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < 2:
                        await asyncio.sleep(10)
                    else:
                        logger.info("Falling back to v9 API...")
                        break

            # If v10 failed, try v9
            try:
                async with self.session.get(
                        f"{self.base_url_v9}{endpoint}",
                        headers=self.headers,
                        params=params
                ) as response:
                    if response.status == 429:
                        data = await response.json()
                        retry_after = data.get('retry_after', 10)
                        await asyncio.sleep(retry_after)
                        return []

                    if response.status == 403:
                        if 'channels' in endpoint:
                            channel_id = endpoint.split('/channels/')[1].split('/')[0]
                            self.inaccessible_channels.add(channel_id)
                            # Update inaccessible channels in users.json

                        return []

                    response.raise_for_status()
                    return await response.json()

            except Exception as e:
                logger.info(f"v9 API attempt also failed: {str(e)}")
                return []


    async def get_user_info(self) -> UserData:
        user_info_dict = await self._make_request("/users/@me")
        return dict_to_dataclass_or_basemodel(UserData, user_info_dict)

    async def get_guilds(self):
        return await self._make_request("/users/@me/guilds")

    async def get_channels(self, guild_id):
        """Get channels with relevance scoring using cached scores when available"""
        try:
            channels = await self._make_request(f"/guilds/{guild_id}/channels")
            if not channels:
                logger.info(f"No channels found for guild {guild_id}")
                return []

            # Filter out inaccessible channels early
            accessible_channels = [
                channel for channel in channels
                if channel['id'] not in self.inaccessible_channels and any(char.isdigit() for char in channel["name"])
            ]

            if not accessible_channels:
                logger.info(f"No accessible channels found in guild {guild_id}")
                return []

            relevant_channels = accessible_channels
            time.sleep(3)

            logger.info(f"Found {len(relevant_channels)} relevant channels out of {len(accessible_channels)} total")
            return relevant_channels

        except Exception as e:
            logger.info(f"Error in get_channels: {e}")
            return []

    async def get_messages(self, channel_id):
        """Get messages from the last 30 minutes"""
        if channel_id in self.inaccessible_channels:
            return []

        # Calculate timestamp for 30 minutes ago
        thirty_mins_ago = datetime.now(timezone.utc) - self.fetch_interval

        # Convert to snowflake ID
        after_snowflake = DiscordAPI._timestamp_to_snowflake(thirty_mins_ago)

        all_messages = []
        params = {
            "limit": 100,
            "after": str(after_snowflake)
        }

        while True:
            logger.info(f"Making request for messages for channel {channel_id}...")
            messages = await self._make_request(f"/channels/{channel_id}/messages", params=params)
            if not messages:
                break

            all_messages.extend(messages)
            logger.info(f"Received {len(messages)}, running total of messages is {len(all_messages)}")
            if len(messages) < 100:
                logger.info(f"Scapred all messages for channel {channel_id}")
                break

            params["after"] = messages[-1]['id']
            await asyncio.sleep(1)  # Rate limit protection

        # Simplified message format without IDs
        formatted_messages = [{
            "content": msg['content'],
            "author_name": msg['author'].get('global_name') or msg['author']['username'],
            "timestamp": msg['timestamp']
        } for msg in all_messages if isinstance(msg, dict)]

        return formatted_messages

    async def process_channel_messages(self, channel, channel_name=None) -> List[MessageData]:
        """Process messages from a single channel"""
        try:
            if not channel or 'id' not in channel:
                return []

            logger.info(f"Processing channel messages for channel {channel['name']}...")
            messages = await self.get_messages(channel['id'])
            logger.info(f"Obtained {len(messages)} messages")
            if not messages:
                return []

            recent_messages = []
            for msg in messages:
                try:
                    if not msg.get('timestamp'):
                        continue

                    msg_time = datetime.fromisoformat(msg['timestamp'].rstrip('Z')).replace(tzinfo=timezone.utc)
                    if msg_time > datetime.now(timezone.utc) - self.fetch_interval:
                        recent_messages.append({
                            **msg,
                            "channel_name": channel_name or channel.get('name', 'Unknown Channel')
                        })

                except Exception as e:
                    logger.info(f"Error processing message in channel {channel.get('name', 'Unknown')}: {e}")
                    continue

            return [
                dict_to_dataclass_or_basemodel(MessageData, message)
                for message in recent_messages
            ]

        except Exception as e:
            logger.info(f"Error processing channel {channel.get('name', 'Unknown')}: {e}")
            return []

    async def get_last_24_hours_messages(self, guild_id) -> Dict[str, List[MessageData]]:
        """Get recent messages concurrently from all channels"""
        channels = await self.get_channels(guild_id)

        # Process channels sequentially
        channel_name_to_messages: Dict[str, List[MessageData]] = {}
        for channel in channels:
            logger.info(f"\nProcessing channel {channel['name']} (id {channel['id']})...")
            channel_name_to_messages[channel["name"]] = await self.process_channel_messages(channel)

            sleep_duration_s = random.randint(1, 15)
            logger.info(f"Sleeping for {sleep_duration_s}s...")
            time.sleep(sleep_duration_s)

        return channel_name_to_messages

    async def process_dm_channel(self, channel) -> List[DMData]:
        """Process messages from a single DM channel"""
        try:
            # Validate channel object
            if not channel or not isinstance(channel, dict) or 'id' not in channel:
                logger.info(f"Invalid channel object: {channel}")
                return []

            # Check if it's a DM channel (type 1) and not already marked inaccessible
            if channel.get('type') != 1:
                logger.info(f"Skipping non-DM channel type: {channel.get('type')}")
                return []

            # Fetch messages with error handling
            try:
                url = f"{self.base_url}/channels/{channel['id']}/messages"
                messages = await self._make_request(f"/channels/{channel['id']}/messages")
            except Exception as e:
                logger.info(f"Failed to fetch messages for channel {channel['id']}: {e}")
                self.inaccessible_channels.add(channel['id'])
                return []

            if not messages:
                logger.info(f"No messages found in channel {channel['id']}")
                return []

            # Filter messages from last 12 days
            thirty_mins_ago = datetime.now(timezone.utc) - timedelta(minutes=30)
            recent_messages = []

            for msg in messages:
                try:
                    msg_time = datetime.fromisoformat(msg['timestamp'].rstrip('Z')).replace(tzinfo=timezone.utc)
                    if msg_time > thirty_mins_ago:
                        recent_messages.append(msg)
                except (ValueError, KeyError) as e:
                    logger.info(f"Error parsing message timestamp: {e}")
                    continue

            logger.info(f"Found {len(recent_messages)} recent messages in channel {channel['id']}")
            return [
                dict_to_dataclass_or_basemodel(DMData, message)
                for message in recent_messages
            ]

        except Exception as e:
            channel_id = channel.get('id', 'unknown') if isinstance(channel, dict) else 'unknown'
            logger.info(f"Error processing DM channel {channel_id}: {e}")
            if isinstance(channel, dict) and 'id' in channel:
                self.inaccessible_channels.add(channel['id'])
            return []

    async def get_private_dms(self) -> List[DMData]:
        logger.info("Fetching DM channels...")
        dm_channels = await self._make_request("/users/@me/channels")
        logger.info(f"Found {len(dm_channels)} DM channels")

        all_dms = []
        for channel in dm_channels:

            messages: List[DMData] = await self.process_dm_channel(channel)

            if not messages:
                logger.info("No messages found in this channel")
                continue

            all_dms.extend(messages)
            logger.info(f"Total messages collected so far: {len(all_dms)}")

        logger.info(f"\nFinal total messages across all DMs: {len(all_dms)}")
        return all_dms

    async def process_guild(self, guild) -> GuildData:
        """Process a single guild's data"""
        try:
            logger.info(f"Processing guild: {guild['name']}")
            channels = await self.get_channels(guild['id'])
            await asyncio.sleep(1)

            channel_name_to_messages = await self.get_last_24_hours_messages(guild['id'])

            guild_data = GuildData(
                guild_name=guild['name'],
                channels=[
                    ChannelData(
                        name=channel.get('name', 'Unknown Channel'),
                        type=channel.get('type'),
                    ) for channel in channels
                ],
                channel_name_to_messages=channel_name_to_messages,
            )
            return guild_data
        except Exception as e:
            logger.info(f"Error processing guild {guild['name']}: {e}")
            return GuildData(
                guild_name=guild['name'],
                channels=[],
                channel_name_to_messages={},
            )


async def fetch_discord_info(
        output_file: str = None
) -> DiscordData:
    user_id = DISCORD_USER_ID
    logger.info(f"User ID: {user_id}")
    discord_api = DiscordAPI(DISCORD_USER_TOKEN, user_id)
    await discord_api.connect()

    try:
        # Get user info
        user_info = await discord_api.get_user_info()

        # Get guilds
        guilds = await discord_api.get_guilds()
        logger.info(f"guilds {guilds}")

        # Get DMs with filtered fields
        filtered_dms: List[DMData] = await discord_api.get_private_dms()
        logger.info(f"filtered_dms {filtered_dms}")

        # Process each guild
        guild_data: List[GuildData] = await asyncio.gather(*[
            discord_api.process_guild(guild) for guild in guilds
        ])

        discord_data = DiscordData(
            user_data=user_info,
            guilds=guild_data,
            dms=filtered_dms,
        )

        if output_file:
            with open(output_file, "w") as f:
                json.dump(convert_to_obj(discord_data), f)
            logger.info(f"Saved messages to {output_file}")

        return discord_data

    finally:
        await discord_api.close()

def get_subnet_from_channel_name(channel_name: str) -> Optional[int]:
    """Get the subnet name from a message"""
    try:
        subnet_id = int(channel_name.split('・')[-1])
        return subnet_id
    except ValueError as e:
        logger.error(f"Failed parsing channel {channel_name} with error {e}")
        return None

class V1DiscordAdapter(BaseDiscordAdapter):
    async def reload_data(self) -> None:
        self.discord_data: DiscordData = await fetch_discord_info()

        channel_name_to_messages: Dict[str, List[MessageData]] = self.discord_data.guilds[0].channel_name_to_messages

        self.subnet_id_to_messages: Dict[int, List[MessageData]] = {}
        for channel_name, messages in channel_name_to_messages.items():
            if "ex" in channel_name:
                continue

            logger.info(f"Trying to parse subnet with channel name '{channel_name}'...")
            subnet_id = get_subnet_from_channel_name(channel_name)
            if not subnet_id:
                continue

            if len(messages) > 0:
                self.subnet_id_to_messages[subnet_id] = messages
            else:
                logger.info(f"No messages exist for subnet {subnet_id}")

    def get_subnet_messages(self, subnet_id: int) -> List[MessageData]:
        return self.subnet_id_to_messages[subnet_id]

    def get_subnet_message_map(self) -> Dict[int, List[MessageData]]:
        return self.subnet_id_to_messages


if __name__ == "__main__":
    asyncio.run(fetch_discord_info(OUTPUT_FILE))
