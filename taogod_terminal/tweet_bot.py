import argparse
import asyncio
import json
import logging
import os
import random
import time
from datetime import timedelta, datetime
from pathlib import Path
from typing import Optional, List, Dict

import pytz
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

from taogod_terminal import summarizer_simple
from taogod_terminal.adapters.discord_adapter import dict_to_dataclass_or_basemodel
from taogod_terminal.summarizer_simple import Tweet

load_dotenv()

consumer_key = os.environ.get("TWITTER_API_KEY")
consumer_secret = os.environ.get("TWITTER_API_SECRET")

oauth1_access_token = os.getenv("TWITTER_OAUTH1_ACCESS_TOKEN")
oauth1_access_token_secret = os.getenv("TWITTER_OAUTH1_ACCESS_TOKEN_SECRET")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

EST = pytz.timezone("US/Eastern")
DAY_START_HOUR = 10  # 10 AM
DAY_END_HOUR = 22  # 10 PM
TWEET_FREQ = timedelta(minutes=60)
SENT_TWEETS_FILE = Path("sent_tweets.json")
TWEETS_DB_REFRESH_DURATION = timedelta(hours=12)


def post_tweet(text: str) -> None:
    payload = {"text": text}

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth1_access_token,
        resource_owner_secret=oauth1_access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    logger.info("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    logger.info(json.dumps(json_response, indent=4, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tweets", type=Path, help="Path to tweets JSON db")
    return parser.parse_args()


async def main(tweets: Optional[Path] = None) -> None:

    tweets_db: Dict[int, List[Tweet]]
    if tweets:
        logger.info(f"Loading old tweets DB from {tweets}")
        with open(tweets, "r") as f:
            tweets_db_raw = json.load(f)
            tweets_db = {
                sn_id: [
                    dict_to_dataclass_or_basemodel(Tweet, tweet)
                    for tweet in tweets
                ]
                for sn_id, tweets in tweets_db_raw.items()
            }
    else:
        logger.info("Generating new tweets DB from Discord scraper:")
        tweets_db = await summarizer_simple.main()
    last_tweets_db_refresh = time.time()

    sent_tweets: List[str]
    if SENT_TWEETS_FILE.is_file():
        with open(SENT_TWEETS_FILE, "r") as f:
            sent_tweets = json.load(f)
    else:
        sent_tweets = []

    time_posted = 0
    while True:
        now = datetime.now(EST)

        if time.time() - last_tweets_db_refresh > TWEETS_DB_REFRESH_DURATION.total_seconds():
            logger.info("Stale DB timeout has passed, regenerating tweets DB from Discord scraper:")
            tweets_db = await summarizer_simple.main()
            last_tweets_db_refresh = time.time()

        if DAY_START_HOUR <= now.hour < DAY_END_HOUR:
            if time.time() - time_posted > TWEET_FREQ.total_seconds():
                sn_id = random.choice(list(tweets_db.keys()))

                if len(tweets_db[sn_id]) == 0:
                    continue

                message: Tweet = random.choice(tweets_db[sn_id])
                while message in sent_tweets or not message.generated_tweet:
                    logger.info(f"message '{message}' invalid; choosing new message")
                    message = random.choice(tweets_db[sn_id])
                logger.info(f"Chose message '{message}'")

                logger.info(f"Creating new post: '{message.generated_tweet}'")
                post_tweet(message.generated_tweet)
                sent_tweets.append(message.generated_tweet)
                with open(SENT_TWEETS_FILE, "w") as f:
                    json.dump(sent_tweets, f)

                time_posted = time.time()

            remaining_time = TWEET_FREQ - (datetime.now() - datetime.fromtimestamp(time_posted))
            next_post_time = datetime.now() + remaining_time
            logger.info(f"Next post will be made at: {next_post_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            next_post_time = datetime.now(EST).replace(hour=DAY_START_HOUR, minute=0, second=0, microsecond=0)
            if now.hour >= DAY_END_HOUR:
                next_post_time += timedelta(days=1)
            logger.info(f"Outside posting hours. Next post will be made at: {next_post_time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(60)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(**vars(args)))
