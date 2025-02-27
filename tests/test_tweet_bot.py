import os
import time
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from taogod_terminal.tweet_bot import parse_args, TWEET_FREQ


@pytest.fixture(autouse=True, scope="session")
def mock_env():
    mock_envars = {
        "TWITTER_API_KEY": "mock_value",
        "TWITTER_API_SECRET": "mock_value",
        "TWITTER_API_BEARER_TOKEN": "mock_value",
        "TWITTER_OAUTH1_ACCESS_TOKEN": "mock_value",
        "TWITTER_OAUTH1_ACCESS_TOKEN_SECRET": "mock_value",
        "DISCORD_USER_TOKEN": "mock_value",
        "DISCORD_USER_ID": "mock_value",
        "ANTHROPIC_API_KEY": "mock_value",
    }
    os.environ.update(mock_envars)

def test_parse_args():
    with patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(tweets=Path("tweets.json"))):
        args = parse_args()
        assert args.tweets == Path("tweets.json")

def test_tweet_frequency_logic():
    last_post_time = time.time() - TWEET_FREQ.total_seconds() - 1
    assert time.time() - last_post_time > TWEET_FREQ.total_seconds()
