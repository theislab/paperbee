from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient


def sample_shortcut_callback(body: dict, ack: Ack, client: WebClient, logger: Logger):
    try:
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "sample_view_id",
                "title": {"type": "plain_text", "text": "Sample modal title"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Click the button to update the modal",
                        },
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Update modal"},
                            "action_id": "sample_action_id",
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "input_block_id",
                        "label": {
                            "type": "plain_text",
                            "text": "What are your hopes and dreams?",
                        },
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "sample_input_id",
                            "multiline": True,
                        },
                    },
                    {
                        "block_id": "select_channel_block_id",
                        "type": "input",
                        "label": {
                            "type": "plain_text",
                            "text": "Select a channel to message the result to",
                        },
                        "element": {
                            "type": "conversations_select",
                            "action_id": "sample_dropdown_id",
                            "response_url_enabled": True,
                        },
                    },
                ],
                "submit": {"type": "plain_text", "text": "Submit"},
            },
        )
    except Exception:
        logger.exception()
