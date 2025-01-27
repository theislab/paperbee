import os

SLACK_CHANNEL_ID: str = os.getenv("SLACK_CHANNEL_ID", "")
SLACK_TEST_CHANNEL_ID: str = os.getenv("SLACK_TEST_CHANNEL_ID", "")
SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN: str = os.getenv("SLACK_APP_TOKEN", "")

TELEGRAM_BOT_API_KEY: str = os.getenv("TELEGRAM_BOT_API_KEY", "")
TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID", "")
TELEGRAM_TEST_CHANNEL_ID: str = os.getenv("TELEGRAM_TEST_CHANNEL_ID", "")

ZULIP_PRC: str = os.getenv("ZULIP_PRC", "")
ZULIP_STREAM: str = os.getenv("ZULIP_STREAM", "")
ZULIP_TOPIC: str = os.getenv("ZULIP_TOPIC", "")

GOOGLE_CREDENTIALS_JSON: str = os.getenv("GOOGLE_CRED_PATH", "")
GOOGLE_SPREADSHEET_ID: str = os.getenv("GOOGLE_CRED_PATH", "")

LOCAL_ROOT_DIR: str = os.getenv("LOCAL_ROOT_DIR", "")

LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
LANGUAGE_MODEL: str = os.getenv("LANGUAGE_MODEL", "")
NCBI_API_KEY: str = os.getenv("NCBI_API_KEY", "")

