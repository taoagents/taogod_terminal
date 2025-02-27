import os

def pytest_configure():
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
