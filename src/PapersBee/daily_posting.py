import argparse
import asyncio
import os
from typing import Any, List, Optional, Tuple

from PapersBee.papers import (
    PapersFinder,
    config,
    validate_configuration,
    validate_llm_args,
    validate_ncbi_api_key,
    validate_posting_args,
)


async def daily_papers_search(interactive: bool = False, since: Optional[int] = None) -> Tuple[List[List[Any]], Any]:
    """
    Searches for daily papers and posts them to Telegram.

    Returns:
        Tuple[List[Dict[str, Any]], Any]: A tuple containing the list of papers and a response object.
    """
    root_dir, query_file, query_file_biorxiv, query_file_pubmed_arxiv = validate_configuration()
    post_to_slack, post_to_zulip, post_to_telegram, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, TELEGRAM_BOT_API_KEY, TELEGRAM_CHANNEL_ID, ZULIP_PRC, ZULIP_STREAM, ZULIP_TOPIC = validate_posting_args()
    llm_filtering = config.llm_filtering
    if llm_filtering:
        filtering_prompt, LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY = validate_llm_args(root_dir)
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
        interactive=interactive,
        llm_filtering=llm_filtering,
        filtering_prompt = filtering_prompt,
        llm_provider=LLM_PROVIDER,
        model=LANGUAGE_MODEL,
        OPENAI_API_KEY=OPENAI_API_KEY,
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
        help="Activate interactive filtering",
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

