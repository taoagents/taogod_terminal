import argparse
import asyncio
import json
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict
from typing import List

import anthropic
from taogod_terminal.adapters.discord_adapter import fetch_discord_info
from taogod_terminal.adapters.github_roadmaps import subnet_roadmaps

from taogod_terminal.adapters.discord_adapter import DiscordData, \
    MessageData, dict_to_dataclass_or_basemodel, convert_to_obj


MAX_DISCORD_MESSAGES = 2000

PROMPT_TEMPLATE = """You are a technical writer creating tweets about cryptocurrency and AI developments.
        
Context about this Bittensor subnet:
{readme_context}

Recent messages in their discord (use this as the primary source!):
{messages_context}

Task: Generate ten tweets of various lengths, topics, etc about this subnet's recent developments. Make it snarky and sound like a zoomer, but focused on the positive aspects of the subnets in a non-sarcastic way. Focus on recent information more. Also, vary the structure of the tweet. The sentence structure should not be repetitive. Also, include either subnet ID or subnet name in every tweet so that people will know which subnet is being discussed just from reading the tweet.

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

def get_subnet_from_channel_name(channel_name: str) -> int:
    """Get the subnet name from a message"""
    return int(channel_name.split('・')[-1])


def generate_tweets_no_simsearch(subnet_number: int, messages: List[MessageData]) -> List[Tweet]:
    readme_context = subnet_roadmaps[subnet_number]
    messages_context = ""

    truncated_messages: List[MessageData] = messages[:MAX_DISCORD_MESSAGES]
    print(f"Adding {len(truncated_messages)} messages for subnet {subnet_number}...")
    for message in truncated_messages:
        if datetime.fromisoformat(message.timestamp) > datetime.now(timezone.utc) - timedelta(days=3):
            messages_context += f"""
                "message": {message.content}
                "timestamp": {message.timestamp}
            """
        print(
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

            for tweet in response.content[0].text.split("\n"):
                tweets.append(Tweet(
                    generated_tweet=tweet,
                    topic="no topic provided",
                    messages_fed_topic=[]
                ))
            print(f"Obtained tweets for subnet {subnet_number}!")
            break
        except Exception as error:
            print("rate limit error", error)
            print("Sleeping for 19 seconds before retrying...")
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

def no_simsearch_loop(discord_data: DiscordData, output_path: Path = None) -> None:
    print("Output path is", output_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    channel_name_to_messages: Dict[str, List[MessageData]] = discord_data.guilds[0].channel_name_to_messages

    tweets_by_subnet: Dict[int, List[Tweet]] = defaultdict(list)
    for channel_name, messages in channel_name_to_messages.items():
        if "ex" in channel_name:
            continue

        print(f"Trying to parse subnet with channel name '{channel_name}'...")
        subnet_id = get_subnet_from_channel_name(channel_name)

        if len(messages) > 0:
            print(f"Generating tweets for subnet {subnet_id}")
            tweets = generate_tweets_no_simsearch(subnet_id, messages)
            print([tweet.generated_tweet for tweet in tweets])
            tweets_by_subnet[subnet_id] = tweets
        else:
            print(f"No messages exist for subnet {subnet_id}")

    if output_path is None:
        output_path = os.path.join(script_dir, 'generated_tweets.json')

    with open(output_path, 'w') as f:
        json.dump(convert_to_obj(tweets_by_subnet), f, indent=2)
    print(f"Results written to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--discord_file", type=Path, help="Path to Discord JSON file")
    parser.add_argument("--output", type=Path, help="Output file for generated tweets")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    if args.discord_file:
        with open(args.discord_file, "r") as f:
            discord_data = dict_to_dataclass_or_basemodel(DiscordData, json.load(f))
    else:
        discord_data = await fetch_discord_info()

    no_simsearch_loop(discord_data, args.output)

if __name__ == "__main__":
    asyncio.run(main())
