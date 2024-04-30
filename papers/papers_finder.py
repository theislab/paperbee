from datetime import date, timedelta
import os
import json
from typing import List, Dict, Any, Tuple
from logging import Logger

import findpapers
import pandas as pd
from slack_sdk import WebClient
from tqdm import tqdm

from .google_sheet import GoogleSheetsUpdater
from .utils import PubMedClient, ArticlesProcessor, parse_date
from .slack_papers_formatter import SlackPaperPublisher
from .telegram_papers_formatter import TelegramPaperPublisher
from .llm_filtering import LLMFilter
from .cli import InteractiveCLIFilter
from . import config


class PapersFinder:
    """
    A class to find, process, and update a list of papers into a Google Sheet.

    Attributes:
        root_dir (str): Directory path where files such as queries and search results are stored.
        spreadsheet_id (str): ID of the Google Spreadsheet to be updated.
        sheet_name (str): Name of the sheet within the Google Spreadsheet to be updated.
        since (date): Start date for the paper search.
        interactive (bool): Activate an interactive cli to filter out papers before posting.
        query (str): a query string to override the query.txt file used in daily automated posting
        channel_id (str): the slack channel id where to post
        since (str): the date from which to start the search formatted as YYYY-mm-dd

    """

    def __init__(
        self,
        root_dir: str,
        spreadsheet_id: str,
        sheet_name: str,
        interactive: bool = False,
        llm_filtering: bool = False,
        query: str = None,
        since: str = None,
        slack_bot_token: str = config.SLACK_BOT_TOKEN,
        slack_channel_id: str = config.SLACK_CHANNEL_ID,
        telegram_bot_token: str = config.SLACK_BOT_TOKEN,
        telegram_channel_id: str = config.SLACK_BOT_TOKEN,
    ) -> None:
        self.root_dir: str = root_dir
        self.spreadsheet_id: str = spreadsheet_id
        self.sheet_name: str = sheet_name
        self.today: date = date.today()
        self.today_str: str = self.today.strftime("%Y-%m-%d")
        self.yesterday: date = self.today - timedelta(days=2)
        self.yesterday_str: str = self.yesterday.strftime("%Y-%m-%d")
        self.until: date = self.today
        self.since: date = self.yesterday if since is None else parse_date(since)
        self.limit: int = 300
        self.limit_per_database: int = 100
        self.databases = ["biorxiv", "arxiv", "pubmed"]
        self.google_credentials_json = config.GOOGLE_CREDENTIALS_JSON
        self.query_file: str = os.path.join(root_dir, "query.txt")
        self.query: str = query
        self.channeld_id: str = slack_channel_id
        self.search_file: str = os.path.join(root_dir, f"{self.today_str}.json")
        self.interactive_filtering: bool = interactive
        self.llm_filtering: bool = llm_filtering
        
        self.slack_bot_token: str = slack_bot_token
        self.slack_channel_id: str = slack_channel_id
        self.slack_publisher = None

        self.telegram_publisher = None
        self.telegram_bot_token: str = telegram_bot_token
        self.telegram_channel_id: str = telegram_channel_id
        self.logger = Logger("PapersFinder")

    def find_and_process_papers(self) -> pd.DataFrame:
        """
        Executes the search for papers based on predefined criteria and processes them.

        Returns:
            pd.DataFrame: A DataFrame containing processed articles.
        """

        with open(self.query_file, "r") as f:
            input_query = f.read().strip()

        if self.query:
            input_query = self.query

        findpapers.search(
            self.search_file,
            input_query,
            self.since,
            self.until,
            self.limit,
            self.limit_per_database,
            self.databases,
            verbose=False,
        )

        with open(self.search_file, "r") as papers_file:
            articles: Dict[str, Any] = json.load(papers_file)["papers"]

        doi_extractor = PubMedClient()
        for article in tqdm(articles):
            if "PubMed" in article["databases"]:
                doi = doi_extractor.get_doi_from_title(article["title"], ncbi_api_key=config.NCBI_API_KEY)
                article["url"] = f"https://doi.org/{doi}" if doi else None
            else:
                article["url"] = next(
                    (s for s in article["urls"] if s.startswith("https://doi.org")),
                    None,
                )
        articles = [article for article in articles if article.get("url") is not None]
        processor = ArticlesProcessor(articles, self.today_str)
        processed_articles = processor.articles

        self.logger.info(f"Found {len(processed_articles)} articles.")

        if self.llm_filtering:
            llm_filter = LLMFilter(processed_articles)
            processed_articles = llm_filter.filter_articles()
            self.logger.info(f"Filtered down to {len(processed_articles)} articles using LLM.")

        if self.interactive_filtering:
            cli = InteractiveCLIFilter(processed_articles)
            processed_articles = cli.filter_articles()
            self.logger.info(f"Filtered down to {len(processed_articles)} articles manually.")

        return processed_articles

    def update_google_sheet(
        self, processed_articles: pd.DataFrame, row: int = 2
    ) -> None:
        """
        Updates the Google Sheet with the processed articles that are not already listed.

        Args:
            processed_articles (pd.DataFrame): DataFrame containing processed articles.
            row (int): The starting row number in the Google Sheet for the updates. Defaults to 2.
        """
        gsheet_updater = GoogleSheetsUpdater(
            spreadsheet_id=self.spreadsheet_id,
            credentials_json_path=self.google_credentials_json,
        )
        gsheet_cache = gsheet_updater.read_sheet_data(sheet_name=self.sheet_name)

        if gsheet_cache:
            published_dois = [article["DOI"] for article in gsheet_cache]

            processed_articles_filtered = processed_articles[
                ~processed_articles["DOI"].isin(published_dois)
            ]
        else:  # Sheet is empty (the moment of deployment)
            processed_articles_filtered = processed_articles

        row_data = [list(row) for row in processed_articles_filtered.values.tolist()]

        if row_data:
            gsheet_updater.insert_rows(sheet_name=self.sheet_name, rows_data=row_data, row=row)
        return row_data

    def post_paper_to_slack(self, papers: List[List[str]]) -> None:
        """
        Posts the papers to Slack.

        Args:
            papers (List[str]): List of papers to post to Slack.
        """
        self.slack_publisher = SlackPaperPublisher(
            WebClient(self.slack_bot_token),
            Logger("SlackPaperPublisher"),
            channel_id=self.channeld_id,
        )

        papers, preprints = self.slack_publisher.format_papers_for_slack(papers)
        response = self.slack_publisher.publish_papers_to_slack(
            papers, preprints, self.today_str, self.spreadsheet_id
        )
        return response
    
    async def post_paper_to_telegram(self, papers: List[List[str]]) -> None:
        """
        Posts the papers to Telegram.

        Args:
            papers (List[str]): List of papers to post to Telegram.
        """
        self.telegram_publisher = TelegramPaperPublisher(
            Logger("TelegramPaperPublisher"),
            channel_id=self.telegram_channel_id,
            bot_token=self.telegram_bot_token,
        )

        papers, preprints = self.telegram_publisher.format_papers(papers)
        response = await self.telegram_publisher.publish_papers(
            papers, preprints, self.today_str, self.spreadsheet_id
        )
        return response

    def cleanup_files(self) -> None:
        """
        Deletes the search result files from the previous day to keep the directory clean.
        """
        yesterday_file = os.path.join(self.root_dir, f"{self.yesterday_str}.json")
        if os.path.exists(yesterday_file):
            os.remove(yesterday_file)
            print(f"Deleted yesterday's file: {yesterday_file}")
        else:
            print(f"File not found, no deletion needed for: {yesterday_file}")

    async def run_daily(self, post_to_slack=True, post_to_telegram=False) -> Tuple[pd.DataFrame, Any]:
        """
        The main method to orchestrate finding, processing, and updating papers in a Google Sheet on a daily schedule.
        """
        processed_articles = self.find_and_process_papers()
        papers = self.update_google_sheet(processed_articles)
        if post_to_slack:
            response = self.post_paper_to_slack(papers)

        if post_to_telegram:
            response = await self.post_paper_to_telegram(papers)

        self.cleanup_files()

        return papers, response

    def send_csv(self, user_id: str, user_query: str) -> Tuple[pd.DataFrame, Any]:
        """
        Paired with search_articles_command listener, send the articles' list as csv file in the channel where it was requested.
        """
        processed_articles = self.find_and_process_papers()
        response = self.slack_publisher._send_csv(
            processed_articles,
            root_dir=self.root_dir,
            user_id=user_id,
            user_query=user_query,
        )
        return processed_articles, response
