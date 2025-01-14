from typing import Any, Dict, List, Tuple

from papers import config
from papers.papers_finder import PapersFinder


async def daily_papers_search() -> Tuple[List[Dict[str, Any]], Any]:
    """
    Searches for daily papers and posts them to Telegram.

    Returns:
        Tuple[List[Dict[str, Any]], Any]: A tuple containing the list of papers and a response object.
    """
    finder = PapersFinder(
        root_dir=config.LOCAL_ROOT_DIR,
        spreadsheet_id=config.GOOGLE_SPREADSHEET_ID,
        sheet_name="Papers",
        llm_filtering=False,
        llm_service = None,
        model = config.OPEN_SOURCE_LLM,
        interactive=False,
        slack_bot_token=config.SLACK_BOT_TOKEN,
        slack_channel_id=config.SLACK_CHANNEL_ID,
        telegram_bot_token=config.TELEGRAM_BOT_API_KEY,
        telegram_channel_id=config.TELEGRAM_CHANNEL_ID,
        zulip_prc=config.ZULIP_PRC,
        zulip_stream=config.ZULIP_STREAM,
        zulip_topic=config.ZULIP_TOPIC,
    )
    papers, response = await finder.run_daily(post_to_slack=False, post_to_telegram=False, post_to_zulip=True)
    return papers, response


if __name__ == "__main__":
    import asyncio

    papers, response = asyncio.run(daily_papers_search())
    print(papers)
    print(response)
