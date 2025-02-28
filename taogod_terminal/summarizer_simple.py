import argparse
import asyncio
import json
import logging
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional
from typing import List

import anthropic
from taogod_terminal.adapters.discord.v1_adapter import V1DiscordAdapter, MessageData, convert_to_obj
from taogod_terminal.adapters.discord.base_adapter import BaseDiscordAdapter
from taogod_terminal.adapters.github.base_adapter import BaseGithubAdapter
from taogod_terminal.adapters.github.static_adapter import StaticGithubAdapter

logger = logging.getLogger(__name__)

MAX_DISCORD_MESSAGES = 2000

PROMPT_TEMPLATE = """You are a technical writer creating tweets about cryptocurrency and AI developments.
        
Context about this Bittensor subnet:
{readme_context}

Recent messages in their discord (use this as the primary source!):
{messages_context}

Task: Generate ten tweets of various lengths, topics, etc about this subnet's recent developments. Make it snarky and sound like a zoomer, but focused on the positive aspects of the subnets in a non-sarcastic way. Focus on recent information more. Also, vary the structure of the tweet. The sentence structure should not be repetitive. Also, include either subnet ID or subnet name in every tweet so that people will know which subnet is being discussed just from reading the tweet. Try to make some of them about dTAO, though not all.

Requirements:
- Must be under 280 characters
- Be technical but accessible
- Include relevant metrics if available
- Don't use hashtags
- Don't include links
- Don't use emojis

Generate only the tweet texts, nothing else."""


@dataclass
class DiscordMessage:
    author_name: str
    content: str
    timestamp: datetime
    channel_name: str
    embedding: List[float]

@dataclass
class Tweet:
    generated_tweet: str
    topic: str
    messages_fed_topic: List[str]

    def __repr__(self) -> str:
        messages = '\n'.join(f"• {msg[:100]}..." for msg in self.messages_fed_topic)
        return (
            f"\n[Topic: {self.topic}]\n"
            f"{self.generated_tweet}\n\n"
            f"Based on:\n{messages}\n"
        )

def get_subnet_from_channel_name(channel_name: str) -> Optional[int]:
    """Get the subnet name from a message"""
    try:
        subnet_id = int(channel_name.split('・')[-1])
        return subnet_id
    except ValueError as e:
        logger.error(f"Failed parsing channel {channel_name} with error {e}")
        return None


def generate_tweets_no_simsearch(subnet_number: int, messages: List[MessageData]) -> List[Tweet]:
    github_adapter: BaseGithubAdapter = StaticGithubAdapter()
    readme_context = github_adapter.get_subnet_roadmap(subnet_number)
    messages_context = ""

    truncated_messages: List[MessageData] = messages[:MAX_DISCORD_MESSAGES]
    logger.info(f"Adding {len(truncated_messages)} messages for subnet {subnet_number}...")
    for message in truncated_messages:
        if datetime.fromisoformat(message.timestamp) > datetime.now(timezone.utc) - timedelta(days=3):
            messages_context += f"""
                "message": {message.content}
                "timestamp": {message.timestamp}
            """
        logger.info(
            f"Template: {len(PROMPT_TEMPLATE)}, messages: {len(messages_context)}, readme: {len(readme_context)}"
            f" Total: {len(PROMPT_TEMPLATE) + len(messages_context) + len(readme_context)}"
        )

    prompt = PROMPT_TEMPLATE.format(
        readme_context=readme_context,
        messages_context=messages_context,
    )
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    tweets = []
    while True:
        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=280,
                temperature=0.7,
                system=prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Generate tweets based on your system prompt. Talk about specific conversations or things, it should not be general."
                            }
                        ]
                    }
                ]
            )

            for tweet in response.content[0].text.split("\n\n")[:-1]:
                tweets.append(Tweet(
                    generated_tweet=tweet,
                    topic="no topic provided",
                    messages_fed_topic=[]
                ))
            logger.info(f"Obtained tweets for subnet {subnet_number}!")
            break
        except Exception as error:
            logger.info("rate limit error", error)
            logger.info("Sleeping for 19 seconds before retrying...")
            time.sleep(19)
            continue

    return tweets

def convert_generated_tweets_into_structured_output(tweets: List[Tweet]):
    return [
        {
            "message": tweet.generated_tweet,
            "topic": tweet.topic,
            "source_messages": tweet.messages_fed_topic
        }
        for tweet in tweets
    ]

def no_simsearch_loop(subnet_id_to_messages: Dict[int, List[MessageData]], output_path: Path = None) -> Dict[int, List[Tweet]]:
    logger.info(f"Output path is {output_path}")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    tweets_by_subnet: Dict[int, List[Tweet]] = defaultdict(list)
    for subnet_id, messages in subnet_id_to_messages.items():
        if len(messages) > 0:
            logger.info(f"Generating tweets for subnet {subnet_id}")
            tweets = generate_tweets_no_simsearch(subnet_id, messages)
            logger.info([tweet.generated_tweet for tweet in tweets])
            tweets_by_subnet[subnet_id] = tweets
        else:
            logger.info(f"No messages exist for subnet {subnet_id}")

    if output_path is None:
        output_path = os.path.join(script_dir, 'generated_tweets.json')

    with open(output_path, 'w') as f:
        json.dump(convert_to_obj(tweets_by_subnet), f, indent=2)
    logger.info(f"Results written to {output_path}")
    return tweets_by_subnet


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Output file for generated tweets")
    return parser.parse_args()


async def main() -> Dict[int, List[Tweet]]:
    args = parse_args()

    discord_adapter: BaseDiscordAdapter = V1DiscordAdapter()
    await discord_adapter.reload_data()
    subnet_id_to_messages = discord_adapter.get_subnet_message_map()

    return no_simsearch_loop(subnet_id_to_messages, args.output)

if __name__ == "__main__":
    asyncio.run(main())
