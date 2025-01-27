import argparse
import asyncio
import os
from typing import Any, Dict, List, Optional, Tuple

from PapersBee.papers import PapersFinder, config


async def daily_papers_search(interactive: bool = False, since: Optional[int] = None) -> Tuple[List[Dict[str, Any]], Any]:  # Modified to accept CLI arguments
    """
    Searches for daily papers and posts them to Telegram.

    Returns:
        Tuple[List[Dict[str, Any]], Any]: A tuple containing the list of papers and a response object.
    """
    root_dir, query_file, query_file_biorxiv, query_file_pubmed_arxiv = validate_configuration()
    post_to_slack, post_to_zulip, post_to_telegram, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, TELEGRAM_BOT_API_KEY, TELEGRAM_CHANNEL_ID, ZULIP_PRC, ZULIP_STREAM, ZULIP_TOPIC = validate_posting_args()
    if interactive:
        #override LLM if interactive is activated
        llm_filtering, LLM_PROVIDER, LANGUAGE_MODEL = None, None, None
    else:
        llm_filtering, LLM_PROVIDER, LANGUAGE_MODEL = validate_llm_args(root_dir)
    validate_ncbi_api_key()

    finder = PapersFinder(
        root_dir=root_dir,
        spreadsheet_id=config.GOOGLE_SPREADSHEET_ID,
        google_credentials_json=config.GOOGLE_CREDENTIALS_JSON,
        sheet_name="Papers",
        since=since,
        query_file=query_file,
        query_file_biorxiv=query_file_biorxiv,
        query_file_pubmed_arxiv=query_file_pubmed_arxiv,
        interactive=False,
        llm_filtering=llm_filtering,
        llm_provider=LLM_PROVIDER,
        model=LANGUAGE_MODEL,
        slack_bot_token=SLACK_BOT_TOKEN,
        slack_channel_id=SLACK_CHANNEL_ID,
        telegram_bot_token=TELEGRAM_BOT_API_KEY,
        telegram_channel_id=TELEGRAM_CHANNEL_ID,
        zulip_prc=ZULIP_PRC,
        zulip_stream=ZULIP_STREAM,
        zulip_topic=ZULIP_TOPIC,
    )
    papers, response = await finder.run_daily(post_to_slack=post_to_slack, post_to_telegram=post_to_telegram, post_to_zulip=post_to_zulip)

    return papers, response


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


def validate_llm_args(root_dir: str) -> Tuple[bool, str, str]:
    if config.LLM_PROVIDER:
        LLM_PROVIDER = config.LLM_PROVIDER
        if LLM_PROVIDER == "openai" and not config.OPENAI_API_KEY:
            e = "OpenAI API key is not set."
            raise ValueError(e)
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
        llm_filtering = True
    elif config.LANGUAGE_MODEL and not config.LLM_PROVIDER:
        e = "Set up LLM provider."
        raise ValueError(e)
    else:
        llm_filtering = False
        LLM_PROVIDER = None
        LANGUAGE_MODEL = None

    return llm_filtering, LLM_PROVIDER, LANGUAGE_MODEL


def validate_ncbi_api_key() -> None:
    if not config.NCBI_API_KEY:
        e = "NCBI API key is not set."
        raise ValueError(e)
    return None


def main() -> None:
    """
    CLI entry point for PapersBee, supporting subcommands like 'post'.
    """
    parser = argparse.ArgumentParser(description="PapersBee CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Subcommand: post
    post_parser = subparsers.add_parser("post", help="Post daily papers")
    post_parser.add_argument(
        "--interactive",
        action="store_true",
        help="Activate interactive filtering, override LLM settings.",
    )
    post_parser.add_argument(
        "--since",
        type=str,
        help="Filter out papers if published before the specified number of days ago.",
    )

    args = parser.parse_args()

    # Dispatch to the appropriate subcommand
    if args.command == "post":
        papers, response = asyncio.run(daily_papers_search(interactive=args.interactive, since=args.since))
        print("Papers found:")
        print(papers)
        print("Response:")
        print(response)

