from telegram import Bot
import pytest

from papers import config

async def send_message(token, chat_id, text):
    bot = Bot(token)
    return bot.sendMessage(chat_id=chat_id, text=text)


@pytest.mark.asyncio
async def test_message_sending():
    message_text = "Bot is working!"
    message = await send_message(config.TELEGRAM_BOT_API_KEY, config.TELEGRAM_TEST_CHANNEL_ID, message_text)

    assert message.message_id is not None

