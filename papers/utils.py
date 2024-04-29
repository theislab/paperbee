from datetime import date, datetime
from typing import List, Union
from time import sleep
import requests

import pandas as pd
import xml.etree.ElementTree as ET


class ArticlesProcessor:
    """
    Processes a list of articles, including filtering columns, extracting DOIs,
    setting dates, determining preprint status, and more.

    Attributes:
        articles (pd.DataFrame): DataFrame containing articles information.
        today_str (str): The current date as a string.

    Methods:
        process_articles(): Process and reshape the input dataframe for the google sheet update.
    """

    def __init__(self, articles: List[dict], today_str: str) -> None:
        """
        Initializes the ArticlesProcessor with articles data and the current date.

        Args:
            articles (List[dict]): A list of dictionaries where each dictionary contains article data.
            today_str (str): The current date formatted as a string.
        """
        self.articles = pd.DataFrame.from_dict(articles)
        self.today_str = today_str
        self.process_articles()

    def process_articles(self) -> None:
        self.filter_columns()
        self.extract_doi()
        self.set_dates()
        self.determine_preprint_status()
        self.rename_and_process_columns()
        self.select_last_columns()

    def filter_columns(self) -> None:
        """Filters the DataFrame to include specific columns."""
        columns = ["databases", "publication_date", "title", "keywords", "url"]
        self.articles = self.articles.loc[:, columns]

    def extract_doi(self) -> None:
        """Extracts DOIs from URLs and adds them as a new column."""
        self.articles["DOI"] = self.articles["url"].apply(lambda x: x[x.find("10.") :])

    def set_dates(self) -> None:
        """Sets the publication date and the date of processing."""
        self.articles["Date"] = self.today_str
        self.articles["PostedDate"] = self.articles["publication_date"]

    def determine_preprint_status(self) -> None:
        """Determines whether each article is a preprint based on its database."""
        self.articles["IsPreprint"] = self.articles["databases"].apply(
            lambda dbs: "FALSE" if "PubMed" in dbs else "TRUE"
        )

    def rename_and_process_columns(self) -> None:
        """Renames columns and processes keywords."""
        self.articles["Title"] = self.articles["title"]
        self.articles["Keywords"] = self.articles["keywords"].apply(
            lambda kws: ", ".join(kw[2:] for kw in kws)
        )
        self.articles["URL"] = self.articles["url"]

    def select_last_columns(self) -> None:
        """Selects and rearranges the final set of columns for the DataFrame."""
        self.articles["Preprint"] = (
            None  # TODO add search for preprint of published articles
        )
        self.articles = self.articles[
            [
                "DOI",
                "Date",
                "PostedDate",
                "IsPreprint",
                "Title",
                "Keywords",
                "Preprint",
                "URL",
            ]
        ]


class PubMedClient:
    """
    A client for fetching DOI (Digital Object Identifier) information for publications from PubMed.
    """

    @staticmethod
    def get_doi_from_title(title: str, seconds_to_wait=1/10, ncbi_api_key=None) -> Union[str, None]:
        """
        Retrieve the DOI (Digital Object Identifier) of a publication given its title by querying PubMed's database.

        Parameters:
        - title (str): The title of the publication.

        Returns:
        - str or None: The DOI of the publication if found, otherwise None.
        """
        if ncbi_api_key:
            api_key = f"&api_key={ncbi_api_key}"
        else:
            api_key = ""

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi?db=pubmed&term={title}&retmode=json{api_key}"
        search_response = requests.get(search_url)
        search_data = search_response.json()

        # NCBI does not allow more than 3 requests per second (10 with an API key)
        if seconds_to_wait:
            sleep(seconds_to_wait)

        pubmed_id = (
            search_data["esearchresult"]["idlist"][0]
            if search_data["esearchresult"]["idlist"]
            else None
        )
        if not pubmed_id:
            return None

        fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
        fetch_response = requests.get(fetch_url)
        root = ET.fromstring(fetch_response.content)

        for article in root.findall(".//Article"):
            for el in article.findall(".//ELocationID"):
                if el.attrib.get("EIdType") == "doi":
                    return el.text
        return None


def parse_date(date_str: Union[str, datetime.date]) -> datetime.date:
    """Parses a string to a datetime.date object."""
    if isinstance(date_str, date):
        return date_str
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(
            f"Invalid date format: {date_str}. Expected YYYY-MM-DD."
        ) from e
