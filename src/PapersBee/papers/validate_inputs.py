import os
from typing import Optional, Tuple

from PapersBee.papers import config
from PapersBee.papers.posting_required_params import SOCIAL_REQUIRED_PARAMS


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

def validate_posting_args() -> Tuple[str, str, str, str, str, str, str]:
    enabled_platforms = [
        ('slack', config.POST_TO_SLACK),
        ('zulip', config.POST_TO_ZULIP),
        ('telegram', config.POST_TO_TELEGRAM),
    ]

    for social, enabled in enabled_platforms:
        if enabled:
            required = SOCIAL_REQUIRED_PARAMS[social]
            missing = [param for param in required if not getattr(config, param, None)]
            if missing:
                e = f"Missing required config params for {social}: {', '.join(missing)}"
                raise ValueError(e)

    return (
        config.SLACK_BOT_TOKEN or "", config.SLACK_CHANNEL_ID or "",
        config.TELEGRAM_BOT_API_KEY or "", config.TELEGRAM_CHANNEL_ID or "",
        config.ZULIP_PRC or "", config.ZULIP_STREAM or "", config.ZULIP_TOPIC or ""
    )


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
            e = f"Invalid LLM provider {LLM_PROVIDER}. Please select one of ('openai', 'ollama')."
            raise ValueError(e)
        LANGUAGE_MODEL = config.LANGUAGE_MODEL
        if not os.path.exists(os.path.join(root_dir, "filtering_prompt.txt")):
            e = "filtering_prompt.txt does not exist in the specified root_dir."
            raise FileNotFoundError(e)
        else:
            with open(os.path.join(root_dir, "filtering_prompt.txt")) as f:
                filtering_prompt = f.read()
    elif config.LANGUAGE_MODEL and not config.LLM_PROVIDER:
        e = "Set up LLM provider."
        raise ValueError(e)
    else:
        e = 'LLM filtering is set to True but LLM_PROVIDER and LANGUAGE_MODEL are not set.'

    return filtering_prompt, LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY


def validate_ncbi_api_key() -> None:
    if not config.NCBI_API_KEY:
        e = "NCBI API key is not set."
        raise ValueError(e)
    return None
