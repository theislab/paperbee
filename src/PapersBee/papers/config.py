import os

SLACK_CHANNEL_ID: str = "C05AGQ467HQ"
SLACK_TEST_CHANNEL_ID: str = "C07045SPWE7"
SLACK_BOT_TOKEN: str = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN: str = os.environ["SLACK_APP_TOKEN"]

TELEGRAM_BOT_API_KEY: str = os.environ["TELEGRAM_BOT_API_KEY"]
TELEGRAM_CHANNEL_ID: str = os.environ["TELEGRAM_CHANNEL_ID"]
TELEGRAM_TEST_CHANNEL_ID: str = os.environ["TELEGRAM_TEST_CHANNEL_ID"]

ZULIP_PRC: str = os.environ["ZULIP_PRC"]
ZULIP_STREAM: str = os.environ["ZULIP_STREAM"]
ZULIP_TOPIC: str = os.environ["ZULIP_TOPIC"]

GOOGLE_CREDENTIALS_JSON: str = os.environ["GOOGLE_CRED_PATH"]
GOOGLE_SPREADSHEET_ID: str = "1vhUam64Rir-dUsoRi-8-QdNSzT22hGGuJmScfgz_3dk"

LOCAL_ROOT_DIR: str = "/Users/vladimir.shitov/Documents/science/sc_papers/"
LOCAL_FILTERING_PROMPT_PATH: str = (
    "/Users/vladimir.shitov/Documents/programming/slack_papers_bot/files/filtering_prompt.txt"
)

OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]



NCBI_API_KEY: str = os.environ["NCBI_API_KEY"]
