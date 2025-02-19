import time
from pathlib import Path
from unittest.mock import patch, MagicMock

from taogod_terminal.tweet_bot import parse_args, TWEET_FREQ


def test_parse_args():
    with patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(tweets=Path("tweets.json"))):
        args = parse_args()
        assert args.tweets == Path("tweets.json")

def test_tweet_frequency_logic():
    last_post_time = time.time() - TWEET_FREQ.total_seconds() - 1
    assert time.time() - last_post_time > TWEET_FREQ.total_seconds()
