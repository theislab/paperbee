import os
from typing import Optional, Tuple

from PapersBee.papers import config


def validate_configuration() -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
    root_dir: str = config.LOCAL_ROOT_DIR
    if not os.path.exists(root_dir):
        e = f"Root directory {root_dir} does not exist."
        raise FileNotFoundError(e)

    if os.path.exists(os.path.join(root_dir, "query.txt")):
        query_file = os.path.join(root_dir, "query.txt")
        query_file_biorxiv = None
        query_file_pubmed_arxiv = None
    else:
        query_file_biorxiv = os.path.join(root_dir, "query_biorxiv.txt")
        query_file_pubmed_arxiv = os.path.join(root_dir, "query_pubmed_arxiv.txt")
        if not (os.path.exists(query_file_biorxiv) and os.path.exists(query_file_pubmed_arxiv)):
            e = "Neither query.txt nor both query_biorxiv.txt and query_pubmed_arxiv.txt exist."
            raise FileNotFoundError(e)
        query_file = None

    if not config.GOOGLE_SPREADSHEET_ID:
        e = "Google Spreadsheet ID is not set."
        raise ValueError(e)
    if not config.GOOGLE_CREDENTIALS_JSON:
        e = "Google credentials JSON is not set."
        raise ValueError(e)

    return root_dir, query_file, query_file_biorxiv, query_file_pubmed_arxiv

def validate_posting_args() -> Tuple[bool, bool, bool, str, str, str, str, str, str, str]:
    post_to_slack, post_to_zulip, post_to_telegram = False, False, False
    SLACK_APP_TOKEN, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID = "", "", ""
    ZULIP_PRC, ZULIP_STREAM, ZULIP_TOPIC = "", "", ""
    TELEGRAM_BOT_API_KEY, TELEGRAM_CHANNEL_ID = "", ""

    if config.SLACK_BOT_TOKEN and config.SLACK_CHANNEL_ID and config.SLACK_APP_TOKEN:
        post_to_slack = True
        SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, SLACK_APP_TOKEN = config.SLACK_BOT_TOKEN, config.SLACK_CHANNEL_ID, config.SLACK_APP_TOKEN
    if config.ZULIP_PRC and config.ZULIP_STREAM and config.ZULIP_TOPIC:
        post_to_zulip = True
        ZULIP_PRC, ZULIP_STREAM, ZULIP_TOPIC = config.ZULIP_PRC, config.ZULIP_STREAM, config.ZULIP_TOPIC
    if config.TELEGRAM_BOT_API_KEY and config.TELEGRAM_CHANNEL_ID:
        post_to_telegram = True
        TELEGRAM_BOT_API_KEY, TELEGRAM_CHANNEL_ID = config.TELEGRAM_BOT_API_KEY, config.TELEGRAM_CHANNEL_ID
    if not post_to_slack and not post_to_zulip and not post_to_telegram:
        e = "Set up at least one of the following: Slack, Zulip, Telegram."
        raise ValueError(e)

    return post_to_slack, post_to_zulip, post_to_telegram, SLACK_BOT_TOKEN or "", SLACK_CHANNEL_ID or "", TELEGRAM_BOT_API_KEY or "", TELEGRAM_CHANNEL_ID or "", ZULIP_PRC or "", ZULIP_STREAM or "", ZULIP_TOPIC or ""


def validate_llm_args(root_dir: str) -> Tuple[bool, str, str, str, str]:
    if config.LLM_PROVIDER:
        LLM_PROVIDER = config.LLM_PROVIDER
        OPENAI_API_KEY = ""
        if LLM_PROVIDER == "openai":
            if not config.OPENAI_API_KEY:
                e = "OpenAI API key is not set."
                raise ValueError(e)
            else:
                OPENAI_API_KEY = config.OPENAI_API_KEY

        if not config.LANGUAGE_MODEL:
            e = "Language model is not set."
            raise ValueError(e)
        if LLM_PROVIDER not in ["openai", "ollama"]:
            e = f"Invalid LLM provider {LLM_PROVIDER}."
            raise ValueError(e)
        LANGUAGE_MODEL = config.LANGUAGE_MODEL
        if not os.path.exists(os.path.join(root_dir, "filtering_prompt.txt")):
            e = "filtering_prompt.txt does not exist in the specified root_dir."
            raise FileNotFoundError(e)
        else:
            with open(os.path.join(root_dir, "filtering_prompt.txt")) as f:
                filtering_prompt = f.read()
        llm_filtering = True
    elif config.LANGUAGE_MODEL and not config.LLM_PROVIDER:
        e = "Set up LLM provider."
        raise ValueError(e)
    else:
        llm_filtering = False
        filtering_prompt = ""
        LLM_PROVIDER = ""
        LANGUAGE_MODEL = ""
        OPENAI_API_KEY = ""

    return llm_filtering, filtering_prompt, LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY


def validate_ncbi_api_key() -> None:
    if not config.NCBI_API_KEY:
        e = "NCBI API key is not set."
        raise ValueError(e)
    return None
