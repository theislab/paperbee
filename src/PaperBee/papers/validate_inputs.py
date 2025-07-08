import os
from typing import Any, Optional, Tuple


def validate_configuration(
    config: dict,
) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
    """
    Validate the root directory, google and NCBI credentials, and the query files.

    Returns:
        Tuple[str, Optional[str], Optional[str], Optional[str]]: A tuple containing the root directory, query file, query file for BioRxiv, and query file for Pubmed and Arxiv.
    """
    root_dir: str = config.get("LOCAL_ROOT_DIR", "")
    if not os.path.exists(root_dir):
        e = f"Root directory {root_dir} does not exist."
        raise FileNotFoundError(e)

    query = config.get("query", "")
    query_biorxiv = config.get("query_biorxiv", "")
    query_pubmed_arxiv = config.get("query_pubmed_arxiv", "")

    if query:
        query_biorxiv = None
        query_pubmed_arxiv = None

    elif query_biorxiv and query_pubmed_arxiv:
        query = None

    else:
        e = "No query is provided. Please set either 'query' or both 'query_biorxiv' and 'query_pubmed_arxiv' in the config file."
        raise FileNotFoundError(e)

    validate_config_variable(config, "GOOGLE_SPREADSHEET_ID")
    validate_config_variable(config, "GOOGLE_CREDENTIALS_JSON")
    validate_config_variable(config, "NCBI_API_KEY")

    return root_dir, query, query_biorxiv, query_pubmed_arxiv


def validate_platform_args(config: dict, platform: str) -> dict[str, Any]:
    """Check that all required platform arguments are set if the posting is enabled."""
    platform_args = config.get(platform)
    if not platform_args:
        e = f"Platform {platform} is not enabled."
        raise ValueError(e)

    if platform_args.get("is_posting_on", False):
        empty_args = [param for param in platform_args if not platform_args[param]]
        if empty_args:
            e = f"Missing required config params for {platform}: {', '.join(empty_args)}"
            raise ValueError(e)
        return dict(platform_args)
    return {}


def validate_llm_args(config: dict, root_dir: str) -> Tuple[str, str, str, str]:
    validate_config_variable(config, "LLM_PROVIDER")
    validate_config_variable(config, "LANGUAGE_MODEL")

    LLM_PROVIDER: str = str(config.get("LLM_PROVIDER", ""))
    OPENAI_API_KEY: str = ""
    if LLM_PROVIDER == "openai":
        validate_config_variable(config, "OPENAI_API_KEY")
        OPENAI_API_KEY = str(config.get("OPENAI_API_KEY", ""))

    if LLM_PROVIDER not in ["openai", "ollama"]:
        e = f"{LLM_PROVIDER} is an invalid LLM provider {LLM_PROVIDER}. Please select one of ('openai', 'ollama')."
        raise ValueError(e)
    LANGUAGE_MODEL: str = str(config.get("LANGUAGE_MODEL", ""))

    filtering_prompt: str = str(config.get("FILTERING_PROMPT", ""))

    return filtering_prompt, LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY


def validate_config_variable(config: dict, var_name: str) -> None:
    """Check if a variable is set in the config dict."""
    value = config.get(var_name)
    if value is None or value == "":
        e = f"{var_name} is not set. Please export {var_name} in your ENV."
        raise ValueError(e)
