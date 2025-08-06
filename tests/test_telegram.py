from logging import Logger

import pytest
import yaml
from telegram import Bot

from PaperBee.papers.telegram_papers_formatter import TelegramPaperPublisher
from tests.sample_papers import sample_papers


async def send_message(token, chat_id, text):
    bot = Bot(token)
    return await bot.send_message(chat_id=chat_id, text=text)


@pytest.fixture
def papers():
    return sample_papers


@pytest.fixture
def publisher():
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)
    return TelegramPaperPublisher(
        logger=Logger("TelegramTest"),
        bot_token=config.get("TELEGRAM")["bot_token"],
        channel_id=config.get("TELEGRAM_TEST_CHANNEL_ID"),
    )


@pytest.mark.asyncio
async def test_message_sending():
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)
    if "your-telegram-bot-token" in config.get("TELEGRAM")["bot_token"]:
        pytest.skip("Telegram config is not set up for integration test.")
    message_text = "Bot is working!"
    message = await send_message(
        config.get("TELEGRAM")["bot_token"],
        config.get("TELEGRAM_TEST_CHANNEL_ID"),
        message_text,
    )

    assert message.message_id is not None


@pytest.mark.asyncio
async def test_publish_papers(publisher, papers):
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)
    if "your-telegram-bot-token" in config.get("TELEGRAM")["bot_token"]:
        pytest.skip("Telegram config is not set up for integration test.")
    papers, preprints = publisher.format_papers(papers)
    message = await publisher.publish_papers(papers, preprints, today=None, spreadsheet_id=None)

    assert message.message_id is not None


@pytest.mark.asyncio
async def test_publish_many_papers(publisher, papers):
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)
    if "your-telegram-bot-token" in config.get("TELEGRAM")["bot_token"]:
        pytest.skip("Telegram config is not set up for integration test.")
    papers, preprints = publisher.format_papers(papers * 10)
    message = await publisher.publish_papers(papers, preprints, today=None, spreadsheet_id=None)

    assert message.message_id is not None
