from papers.papers_finder import PapersFinder

from papers import config


finder = PapersFinder(
    root_dir=config.LOCAL_ROOT_DIR,
    spreadsheet_id=config.GOOGLE_SPREADSHEET_ID,
    sheet_name="Papers",
    llm_filtering=True,
    interactive=False,
    slack_bot_token=config.SLACK_BOT_TOKEN,
    slack_channel_id=config.SLACK_CHANNEL_ID,
    telegram_bot_token=config.SLACK_BOT_TOKEN,
    telegram_channel_id=config.SLACK_BOT_TOKEN,
)
papers, response = finder.run_daily(post_to_slack=True, post_to_telegram=True)
