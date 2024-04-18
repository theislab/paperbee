from papers.papers_finder import PapersFinder


finder = PapersFinder(
    root_dir="/home/daniele/Code/slack-papers-app/files/",
    spreadsheet_id="1WV8xjZnUbWpM26nJvs7_fFkh3f2TZuBRdOnI2WUFgEs",
    sheet_name="Papers",
    interactive=True,
)
papers, response = finder.run_daily()
