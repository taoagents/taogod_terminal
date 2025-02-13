import argparse
import json
import os
import random
import time
from datetime import timedelta, datetime
from pathlib import Path

import pytz
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()

consumer_key = os.environ.get("TWITTER_API_KEY")
consumer_secret = os.environ.get("TWITTER_API_SECRET")

oauth1_access_token = os.getenv("TWITTER_OAUTH1_ACCESS_TOKEN")
oauth1_access_token_secret = os.getenv("TWITTER_OAUTH1_ACCESS_TOKEN_SECRET")


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

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


EST = pytz.timezone("US/Eastern")
DAY_START_HOUR = 10  # 10 AM
DAY_END_HOUR = 22  # 10 PM
TWEET_FREQ = timedelta(minutes=60)
SENT_TWEETS_FILE = Path("sent_tweets.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tweets", type=Path, required=True, help="Path to tweets JSON db")
    return parser.parse_args()


def main(tweets: Path):
    with open(tweets, "r") as f:
        tweets_db = json.load(f)

    if SENT_TWEETS_FILE.is_file():
        with open(SENT_TWEETS_FILE, "r") as f:
            sent_tweets = json.load(f)
    else:
        sent_tweets = []

    time_posted = 0
    while True:
        now = datetime.now(EST)
        if DAY_START_HOUR <= now.hour < DAY_END_HOUR:
            if time.time() - time_posted > TWEET_FREQ.total_seconds():
                sn_id = random.choice(list(tweets_db.keys()))

                message = random.choice(tweets_db[sn_id])
                while message in sent_tweets or not message["message"]:
                    print(f"message '{message}' invalid; choosing new message")
                    message = random.choice(tweets_db[sn_id])
                print(f"Chose message '{message}'")

                print(f"Creating new post: '{message['message']}'")
                post_tweet(message["message"])
                sent_tweets.append(message)
                with open(SENT_TWEETS_FILE, "w") as f:
                    json.dump(sent_tweets, f)

                time_posted = time.time()

            remaining_time = TWEET_FREQ - (datetime.now() - datetime.fromtimestamp(time_posted))
            next_post_time = datetime.now() + remaining_time
            print(f"Next post will be made at:", next_post_time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            next_post_time = datetime.now(EST).replace(hour=DAY_START_HOUR, minute=0, second=0, microsecond=0)
            if now.hour >= DAY_END_HOUR:
                next_post_time += timedelta(days=1)
            print(f"Outside posting hours. Next post will be made at:", next_post_time.strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(60)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
