from papers.papers_finder import PapersFinder

from papers import config


finder = PapersFinder(
    root_dir=config.LOCAL_ROOT_DIR,
    spreadsheet_id=config.GOOGLE_SPREADSHEET_ID,
    sheet_name="Papers",
    llm_filtering=True,
    interactive=False,
)
papers, response = finder.run_daily()
