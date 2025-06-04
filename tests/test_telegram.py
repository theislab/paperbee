from telegram import Bot
import pytest
from logging import Logger
import yaml

from PaperBee.papers.telegram_papers_formatter import TelegramPaperPublisher

async def send_message(token, chat_id, text):
    bot = Bot(token)
    return await bot.send_message(chat_id=chat_id, text=text)

@pytest.fixture
def papers():
    return [
        ["10.1101/2024.04.26.591400", "2024-04-29", "2024-04-28", "TRUE", "Single-Cell Transcriptomics Reveals the Molecular Logic Underlying Ca2+ Signaling Diversity in Human and Mouse Brain", "https://doi.org/10.1101/2024.04.26.591400"],
        ["10.1101/2024.04.22.590645", "2024-04-29", "2024-04-26", "TRUE", "scMUSCL: Multi-Source Transfer Learning for Clustering scRNA-seq Data", "https://doi.org/10.1101/2024.04.22.590645"],
        ["10.1101/2024.04.21.590442", "2024-04-29", "2024-04-26", "TRUE", "Imbalance and Composition Correction Ensemble Learning Framework (ICCELF): A novel framework for automated scRNA-seq cell type annotation", "https://doi.org/10.1101/2024.04.21.590442"],
    ]

@pytest.fixture
def publisher():
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)
    return TelegramPaperPublisher(logger=Logger("TelegramTest"), bot_token=config.get("TELEGRAM")["bot_token"], channel_id=config.get("TELEGRAM_TEST_CHANNEL_ID"))

@pytest.mark.asyncio
async def test_message_sending():
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)
    message_text = "Bot is working!"
    message = await send_message(config.get("TELEGRAM")["bot_token"], config.get("TELEGRAM_TEST_CHANNEL_ID"), message_text)

    assert message.message_id is not None

@pytest.mark.asyncio
async def test_publish_papers(publisher, papers):
    papers, preprints = publisher.format_papers(papers)
    message = await publisher.publish_papers(papers, preprints, today=None, spreadsheet_id=None)

    assert message.message_id is not None

@pytest.mark.asyncio
async def test_publish_many_papers(publisher, papers):
    papers, preprints = publisher.format_papers(papers * 10)
    message = await publisher.publish_papers(papers, preprints, today=None, spreadsheet_id=None)

    assert message.message_id is not None
