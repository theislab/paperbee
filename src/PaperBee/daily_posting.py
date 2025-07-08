import argparse
import asyncio
from typing import Any, List, Optional, Tuple, cast

import yaml

from PaperBee.papers import (
    PapersFinder,
    validate_configuration,
    validate_llm_args,
    validate_platform_args,
)


def load_config(config_path: str) -> dict[Any, Any]:
    with open(config_path) as f:
        return cast(dict[Any, Any], yaml.safe_load(f))


async def daily_papers_search(
    config: dict,
    interactive: bool = False,
    since: Optional[int] = None,
    databases: Optional[List[str]] = None,
) -> Tuple[List[List[Any]], Any, Any, Any]:
    """
    Searches for daily papers and posts them to Telegram.

    Returns:
        Tuple[List[List[Any]], Any, Any, Any]:
            - List of papers (list of lists of Any)
            - Slack response
            - Telegram response
            - Zulip response
    """
    root_dir, query, query_biorxiv, query_pubmed_arxiv = validate_configuration(config)

    slack_args = validate_platform_args(config, "SLACK")
    zulip_args = validate_platform_args(config, "ZULIP")
    telegram_args = validate_platform_args(config, "TELEGRAM")

    print(slack_args, zulip_args, telegram_args)

    if telegram_args == {}:
        telegram_args = {"bot_token": "", "channel_id": "", "is_posting_on": False}
    if zulip_args == {}:
        zulip_args = {"prc": "", "stream": "", "topic": "", "is_posting_on": False}
    if slack_args == {}:
        slack_args = {"bot_token": "", "channel_id": "", "is_posting_on": False}

    print(slack_args, zulip_args, telegram_args)
    llm_filtering = config.get("LLM_FILTERING", False)
    if llm_filtering:
        filtering_prompt, LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY = validate_llm_args(config, root_dir)
    else:
        filtering_prompt = ""
        LLM_PROVIDER = ""
        LANGUAGE_MODEL = ""
        OPENAI_API_KEY = ""

    finder = PapersFinder(
        root_dir=root_dir,
        spreadsheet_id=config.get("GOOGLE_SPREADSHEET_ID", ""),
        google_credentials_json=config.get("GOOGLE_CREDENTIALS_JSON", ""),
        sheet_name="Papers",
        since=since,
        query=query,
        query_biorxiv=query_biorxiv,
        query_pubmed_arxiv=query_pubmed_arxiv,
        interactive=interactive,
        llm_filtering=llm_filtering,
        filtering_prompt=filtering_prompt,
        llm_provider=LLM_PROVIDER,
        model=LANGUAGE_MODEL,
        OPENAI_API_KEY=OPENAI_API_KEY,
        slack_bot_token=slack_args["bot_token"],
        slack_channel_id=slack_args["channel_id"],
        telegram_bot_token=telegram_args["bot_token"],
        telegram_channel_id=telegram_args["channel_id"],
        zulip_prc=zulip_args["prc"],
        zulip_stream=zulip_args["stream"],
        zulip_topic=zulip_args["topic"],
        databases=databases,
    )
    papers, response_slack, response_telegram, response_zulip = await finder.run_daily(
        post_to_slack=slack_args["is_posting_on"],
        post_to_telegram=telegram_args["is_posting_on"],
        post_to_zulip=zulip_args["is_posting_on"],
    )

    return papers, response_slack, response_telegram, response_zulip


def main() -> None:
    """
    CLI entry point for PaperBee, supporting subcommands like 'post'.
    """
    parser = argparse.ArgumentParser(description="PaperBee CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Subcommand: post
    post_parser = subparsers.add_parser("post", help="Post daily papers")
    post_parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to YAML configuration file.",
    )
    post_parser.add_argument(
        "--interactive",
        action="store_true",
        help="Activate interactive filtering",
    )
    post_parser.add_argument(
        "--since",
        type=int,
        help="Filter out papers if published before the specified number of days ago.",
    )
    post_parser.add_argument(
        "--databases",
        nargs="+",
        type=str,
        help="Specify any combination of databases to search among the available ones 'pubmed','arxiv', and 'biorxiv'(e.g., ['pubmed', 'arxiv']).",
    )
    args = parser.parse_args()

    # Dispatch to the appropriate subcommand
    if args.command == "post":
        config = load_config(args.config)
        papers, response_slack, response_telegram, response_zulip = asyncio.run(
            daily_papers_search(
                config,
                interactive=args.interactive,
                since=args.since,
                databases=args.databases,
            )
        )
        print("Papers found:")
        print(papers)
