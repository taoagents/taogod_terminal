# Taogod Terminal Bittensor Twitter Bot

## Overview
This repository contains scripts to automate tweet generation and posting for cryptocurrency and AI developments, specifically targeting Bittensor subnets. The bot gathers recent messages from Discord channels, processes them, and generates snarky yet informative tweets.

## Features
- **Automated Tweet Posting**: Tweets are posted between 10 AM and 10 PM (Eastern Time) at hourly intervals.
- **Tweet Generation**: Uses Anthropic's Claude model to generate tweets from recent Discord messages.
- **Filtering and Formatting**: Ensures tweets stay under 280 characters, maintain accessibility, and follow predefined stylistic constraints.
- **JSON-Based Storage**: Keeps track of sent tweets to avoid duplicates.

## Requirements
- Python 3.9+

## Setup
1. Install repository: `pip install -e .`
2. Set envars in `.env` file, see `.env.example`.
3. Collect discord data via the `discord_adapter.py` script
4. Generate future tweets using the `summerizer_simple.py` script.
3. Run the tweet poster script:
   ```sh
   python tweet_bot.py --tweets path/to/tweets.json
   ```

## Customization
- Adjust posting frequency by modifying `TWEET_FREQ` in `tweet_poster.py`.
- Modify tweet generation rules by tweaking `PROMPT_TEMPLATE` in `generate_tweets.py`.
- Add more filtering logic in `generate_tweets_no_simsearch()` if needed.

## Troubleshooting
- **Rate Limits**: If hitting Twitter API rate limits, increase `TWEET_FREQ` or handle retries with backoff logic.
- **Anthropic API Issues**: If tweet generation fails, check API usage limits or tweak parameters.
- **Invalid Tweets**: Ensure the Discord messages used for generation are valid and well-formatted.

## Contributing
Feel free to submit issues or pull requests to improve functionality.

## License
MIT License.