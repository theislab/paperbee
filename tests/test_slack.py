import yaml

import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# The function to send messages
def send_message(config, client, message):
    response = client.chat_postMessage(channel=config.get("SLACK_TEST_CHANNEL_ID"), text=message)
    if response["ok"]:
        return response["message"]["text"]
    else:
        raise SlackApiError("Error sending message", response)

# The actual test
@pytest.mark.integration
def test_slack_integration():
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)

    client = WebClient(token=config.get("SLACK")["bot_token"])

    print("Bot token:", config.get("SLACK")["bot_token"])

    # Test sending a message
    sent_message = "The bot is working!"
    received_message = send_message(config, client, sent_message)

    assert received_message == sent_message, "The message sent should match the message received"

