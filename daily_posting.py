from papers.papers_finder import PapersFinder

from papers import config
async def daily_papers_search():
    finder = PapersFinder(
    root_dir=config.LOCAL_ROOT_DIR,
    spreadsheet_id=config.GOOGLE_SPREADSHEET_ID,
    sheet_name="Papers",
    llm_filtering=True,
    interactive=False,
    slack_bot_token=config.SLACK_BOT_TOKEN,
    slack_channel_id=config.SLACK_CHANNEL_ID,
    telegram_bot_token=config.TELEGRAM_BOT_API_KEY,
    telegram_channel_id=config.TELEGRAM_CHANNEL_ID,
)
    papers, response = await finder.run_daily(post_to_slack=False, post_to_telegram=True)
    return papers, response

if __name__ == "__main__":
    import asyncio

    papers, response = asyncio.run(daily_papers_search())
    print(papers)
    print(response)