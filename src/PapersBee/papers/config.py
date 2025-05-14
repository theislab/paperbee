import os

SLACK: dict = {
    "is_posting_on": os.getenv("POST_TO_SLACK", "False").lower() == "true",
    "channel_id": os.getenv("SLACK_CHANNEL_ID", ""),
    "bot_token": os.getenv("SLACK_BOT_TOKEN", ""),
    "app_token": os.getenv("SLACK_APP_TOKEN", ""),
}
SLACK_TEST_CHANNEL_ID: str = os.getenv("SLACK_TEST_CHANNEL_ID", "")  # not required so left outside of dictionary

TELEGRAM: dict = {
    "is_posting_on": os.getenv("POST_TO_TELEGRAM", "False").lower() == "true",
    "bot_token": os.getenv("TELEGRAM_BOT_API_KEY", ""),
    "channel_id": os.getenv("TELEGRAM_CHANNEL_ID", ""),
}
TELEGRAM_TEST_CHANNEL_ID: str = os.getenv("TELEGRAM_TEST_CHANNEL_ID", "") # not required so left outside of dictionary

ZULIP: dict = {
    "is_posting_on": os.getenv("POST_TO_ZULIP", "False").lower() == "true",
    "prc": os.getenv("ZULIP_PRC", ""),
    "stream": os.getenv("ZULIP_STREAM", ""),
    "topic": os.getenv("ZULIP_TOPIC", ""),
}

GOOGLE_CREDENTIALS_JSON: str = os.getenv("GOOGLE_CRED_PATH", "")
GOOGLE_SPREADSHEET_ID: str = os.getenv("GOOGLE_SPREADSHEET_ID", "")
GOOGLE_TEST_SPREADSHEET_ID: str = os.getenv("GOOGLE_TEST_SPREADSHEET_ID", "")

LOCAL_ROOT_DIR: str = os.getenv("LOCAL_ROOT_DIR", "")

LLM_FILTERING: bool = os.getenv("LLM_FILTERING", "False").lower() == "true"
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
LANGUAGE_MODEL: str = os.getenv("LANGUAGE_MODEL", "")
NCBI_API_KEY: str = os.getenv("NCBI_API_KEY", "")
