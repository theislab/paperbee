import os
from logging import Logger
from typing import Any, List, Optional, Tuple

import pandas as pd
import zulip


class ZulipPaperPublisher:
    """
    A class to manage publishing academic papers to a Zulip stream.

    Args:
        client (zulip.Client): A Zulip client instance for interacting with Zulip's API.
        logger (Logger): A logger instance for logging information and errors.
        stream_name (Optional[str]): The name of the Zulip stream where papers will be published.
        topic_name (Optional[str]): The topic within the Zulip stream where papers will be posted.
    """

    def __init__(
        self,
        logger: Logger,
        prc: str,
        stream_name: str,
        topic_name: str,
    ) -> None:
        """
        Initializes the ZulipPaperPublisher with the Zulip client, logger, and optional stream/topic names.

        Args:
            logger (Logger): The logger instance for logging messages.
            stream_name (str): The name of the Zulip stream.
            topic_name (str): The topic name.
        """
        self.client = zulip.Client(config_file=prc)
        self.logger = logger
        self.stream_name = stream_name
        self.topic_name = topic_name

    @staticmethod
    def format_papers_for_zulip(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
        """
        Formats a list of papers into separate lists for regular papers and preprints with Zulip message formatting.

        Args:
            papers_list (List[List[str]]): A list of papers, where each paper is a list of attributes.

        Returns:
            Tuple[List[str], List[str]]: Two lists, one for regular papers and one for preprints, each formatted for Zulip.
        """
        papers = []
        preprints = []
        for paper in papers_list:
            emoji = "🖊️" if paper[3] == "TRUE" else "📰"
            formatted_paper = f"{emoji} [{paper[4]}]({paper[-1]})"
            if paper[3] == "TRUE":
                preprints.append(formatted_paper)
            else:
                papers.append(formatted_paper)

        return papers, preprints

    async def publish_papers_to_zulip(
        self,
        papers: List[str],
        preprints: List[str],
        today: str,
        spreadsheet_id: str,
    ) -> Optional[Any]:
        """
        Publishes the formatted papers and preprints to the specified Zulip stream and topic.

        Args:
            papers (List[str]): A list of formatted regular papers.
            preprints (List[str]): A list of formatted preprints.
            today (str): The date for the publication (used in the message header).
            spreadsheet_id (str): The ID of the Google Spreadsheet containing the papers.

        Returns:
            Optional[Any]: The Zulip API response on success, or None if there is an error.
        """
        if not self.stream_name:
            self.logger.error("Stream name is not provided.")
            return None

        try:
            header = f"Good morning ☕ Here are today's papers ({today})! 📚\n\n"
            footer = f"View all papers: [Google Sheet](https://docs.google.com/spreadsheets/d/{spreadsheet_id}) 📖"

            message_body = header

            # Add preprints
            message_body += "**Preprints:** :point_down:\n\n"
            if preprints:
                message_body += "\n".join(preprints)
            else:
                message_body += "No preprints found today.\n"

            message_body += "\n\n---\n\n"

            # Add regular papers
            message_body += "**Papers:** :point_down:\n\n"
            if papers:
                message_body += "\n".join(papers)
            else:
                message_body += "No papers found today.\n"

            message_body += f"\n\n---\n\n{footer}"

            # Send the message to Zulip
            response = self.client.send_message({
                "type": "stream",
                "to": self.stream_name,
                "topic": self.topic_name,
                "content": message_body,
            })

            self.logger.info(f"Published papers to Zulip: {response}")
        except Exception:
            self.logger.exception("Error in publishing papers to Zulip:", exc_info=True)
            return None
        else:
            return response

    def _send_csv(self, papers: pd.DataFrame, root_dir: str, user_email: str, user_query: str) -> Optional[Any]:
        """
        Sends a CSV file of papers to the specified Zulip user via private message.

        Args:
            papers (pd.DataFrame): The DataFrame containing the papers to be sent.
            root_dir (str): The root directory where the CSV file will be temporarily saved.
            user_email (str): The Zulip email of the person who requested the CSV.
            user_query (str): The query string used by the user to filter papers.

        Returns:
            Optional[Any]: The Zulip API response on success, or None if there is an error.
        """
        csv_path = os.path.join(root_dir, f"{user_email}_requested_papers.csv")
        papers.to_csv(csv_path, index=False)

        try:
            with open(csv_path, "rb") as file:
                response = self.client.send_message({
                    "type": "private",
                    "to": user_email,
                    "content": f"Here is the CSV file of papers based on your query: '{user_query}'",
                    "file": file,
                })
            self.logger.info(f"Successfully uploaded papers CSV to Zulip: {response}")
        except Exception:
            self.logger.exception("Error encountered while sending CSV file to Zulip.", exc_info=True)
            return None
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)
        return response
