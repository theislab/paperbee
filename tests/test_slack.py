import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from papers import config

# The function to send messages
def send_message(client, message):
    response = client.chat_postMessage(channel=config.SLACK_TEST_CHANNEL_ID, text=message)
    if response["ok"]:
        return response["message"]["text"]
    else:
        raise SlackApiError("Error sending message", response)

# The actual test
@pytest.mark.integration
def test_slack_integration():
    client = WebClient(token=config.SLACK_BOT_TOKEN)

    print("Bot token:", config.SLACK_BOT_TOKEN)

    # Test sending a message
    sent_message = "The bot is working!"
    received_message = send_message(client, sent_message)

    assert received_message == sent_message, "The message sent should match the message received"

