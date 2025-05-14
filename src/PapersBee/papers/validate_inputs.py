import os
from typing import Optional, Tuple

from PapersBee.papers import config


def validate_configuration() -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
    """
    Validate the root directory, google and NCBI credentials, and the query files.

    Returns:
        Tuple[str, Optional[str], Optional[str], Optional[str]]: A tuple containing the root directory, query file, query file for BioRxiv, and query file for Pubmed and Arxiv.
    """
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

def validate_platform_args(platform: str) -> Tuple[str, ...]:
    """Check that all required platform arguments are set if the posting is enabled."""

    platform_args = getattr(config, platform, None)

    if not platform_args:
        raise ValueError(f"Platform {platform} is not enabled.")

    if platform_args["is_posting_on"]:
        empty_args = [param for param in platform_args if not platform_args[param]]
        if empty_args:
            e = f"Missing required config params for {platform}: {', '.join(empty_args)}"
            raise ValueError(e)
        
    return platform_args


def validate_llm_args(root_dir: str) -> Tuple[bool, str, str, str, str]:
    validate_config_variable('LLM_PROVIDER')
    validate_config_variable('LANGUAGE_MODEL')

    LLM_PROVIDER = config.LLM_PROVIDER
    OPENAI_API_KEY = ""
    if LLM_PROVIDER == "openai":
        validate_config_variable("OPENAI_API_KEY")
        OPENAI_API_KEY = config.OPENAI_API_KEY

    if LLM_PROVIDER not in ["openai", "ollama"]:
        e = f"{LLM_PROVIDER} is an invalid LLM provider {LLM_PROVIDER}. Please select one of ('openai', 'ollama')."
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
    """Check if a variable is set in python or in the environment."""
    value = getattr(config, var_name, None)
    if value is None or value == "":
        e = f"{var_name} is not set. Please export {var_name} in your ENV."
        raise ValueError(e)

