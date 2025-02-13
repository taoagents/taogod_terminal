import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from pprint import pprint
from typing import Dict
from typing import List

import anthropic

from taogod_terminal.adapters.github_roadmaps import subnet_roadmaps

MAX_DISCORD_MESSAGES = 2000
subnet_channel_id_map = {}

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

def get_subnet_from_message(message: Dict) -> int:
    """Get the subnet name from a message"""
    return int(message['channel_name'].split('・')[-1])


def generate_tweets_no_simsearch(subnet_number: int, raw_messages_json) -> List[Tweet]:
    channel_id = subnet_channel_id_map[subnet_number]
    raw_messages = raw_messages_json[channel_id]

    readme_context = subnet_roadmaps[subnet_number]
    messages_context = ""

    truncated_messages = raw_messages[:MAX_DISCORD_MESSAGES]
    print(f"Adding {len(truncated_messages)} messages for subnet {subnet_number}...")
    for message in truncated_messages:
        if datetime.fromisoformat(message["timestamp"]) > datetime.now(timezone.utc) - timedelta(days=3):
            messages_context += f"""
                "message": {message['content']}
                "timestamp": {message['timestamp']}
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

def no_simsearch_loop(json_path: Path, output_path: Path = None) -> None:
    print("Output path is", output_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Read and display first few lines of discord.json
    with open(json_path) as f:
        data = json.load(f)

        for i in range(len(list(data))):
            messages_in_channel = data[list(data)[i]]
            channel_id = list(data)[i]

            if len(messages_in_channel) > 0:
                channel_name = messages_in_channel[0]['channel_name']

                if 'ex' in channel_name:
                    continue

                channel_subnet_id = get_subnet_from_message(messages_in_channel[0])

                subnet_channel_id_map[channel_subnet_id] = channel_id
        
        print("Generated channel map:")
        pprint(subnet_channel_id_map, indent=2)
        print("\n\n")
        existing_subnets = subnet_roadmaps.keys()
        tweets_by_subnet = {}

        for subnet in existing_subnets:
            if subnet not in subnet_channel_id_map:
                print(f"Skipping subnet {subnet} because there is no associated channel map")
                continue

            print(f"Generating tweets for subnet {subnet}")
            tweets = generate_tweets_no_simsearch(subnet, data)
            print([tweet.generated_tweet for tweet in tweets])
            tweets_by_subnet[subnet] = convert_generated_tweets_into_structured_output(tweets)


    if output_path is None:
        output_path = os.path.join(script_dir, 'generated_tweets.json')

    with open(output_path, 'w') as f:
        json.dump(tweets_by_subnet, f, indent=2)
    print(f"Results written to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("discord_file", type=Path, help="Path to Discord JSON file")
    parser.add_argument("--output", type=Path, help="Output file for generated tweets")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    no_simsearch_loop(args.discord_file, args.output)
