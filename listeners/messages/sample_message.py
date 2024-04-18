from logging import Logger

from slack_bolt import BoltContext, Say
from slack_sdk import WebClient


def sample_message_callback(
    context: BoltContext, client: WebClient, say: Say, logger: Logger
):
    try:
        _ = context["matches"][0]  # disable
        # say(f"{greeting}, how are you?")
    except Exception as e:
        logger.error(e)
