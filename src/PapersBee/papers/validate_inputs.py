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

    validate_config_variable("GOOGLE_SPREADSHEET_ID")
    validate_config_variable("GOOGLE_CREDENTIALS_JSON")
    validate_config_variable('NCBI_API_KEY')

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
    validate_config_variable('LLM_PROVIDER')
    validate_config_variable('LANGUAGE_MODEL')

    LLM_PROVIDER = config.LLM_PROVIDER
    OPENAI_API_KEY = ""
    if LLM_PROVIDER == "openai":
        validate_config_variable("OPENAI_API_KEY")
        OPENAI_API_KEY = config.OPENAI_API_KEY

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

    return filtering_prompt, LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY


def validate_config_variable(var_name):
    value = getattr(config, var_name, None)
    if value is None or value == "":
        e = f"{var_name} is not set. Please export {var_name} in your ENV."
        raise ValueError(e)

