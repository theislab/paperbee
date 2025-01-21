import logging
import os
from typing import Any, Callable, Dict

from listeners import register_listeners
from papers import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialization
app = App(token=config.SLACK_BOT_TOKEN)
logging.basicConfig(level=logging.DEBUG)

# Register Listeners
register_listeners(app)


@app.message("hello")
def message_hello(message: Dict[str, Any], say: Callable[..., Any]) -> None:
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey there <@{message['user']}>!",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
