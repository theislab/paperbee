import os
from logging import Logger
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse


class SlackPaperPublisher:
    """
    A class to manage publishing academic papers to a Slack channel.

    Args:
        client (WebClient): A Slack WebClient instance for interacting with Slack's API.
        logger (Logger): A logger instance for logging information and errors.
        channel_id (Optional[str]): The ID of the Slack channel where papers will be published.
    """

    def __init__(self, client: WebClient, logger: Logger, channel_id: Optional[str] = None) -> None:
        """
        Initializes the SlackPaperPublisher with the Slack client, logger, and optional channel ID.

        Args:
            client (WebClient): The Slack WebClient instance.
            logger (Logger): The logger instance for logging messages.
            channel_id (Optional[str]): The ID of the Slack channel. Defaults to None.
        """
        self.client = client
        self.logger = logger
        self.channel_id = channel_id

    @staticmethod
    def format_papers_for_slack(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
        """
        Formats a list of papers into separate lists for regular papers and preprints with Slack message formatting.

        Args:
            papers_list (List[List[str]]): A list of papers, where each paper is a list of Args.

        Returns:
            Tuple[List[str], List[str]]: Two lists, one for regular papers and one for preprints, each formatted for Slack.
        """
        papers = []
        preprints = []
        for paper in papers_list:
            emoji = ":pencil:" if paper[3] == "TRUE" else ":rolled_up_newspaper:"
            formatted_paper = f"{emoji} <{paper[-1]}|{paper[4]}>"
            if paper[3] == "TRUE":
                preprints.append(formatted_paper)
            else:
                papers.append(formatted_paper)

        return papers, preprints

    def publish_papers_to_slack(
        self,
        papers: List[str],
        preprints: List[str],
        today: str,
        spreadsheet_id: str,
    ) -> Optional[SlackResponse]:
        """
        Publishes the formatted papers and preprints to the specified Slack channel.

        Args:
            papers (List[str]): A list of formatted regular papers.
            preprints (List[str]): A list of formatted preprints.
            today (str): The date for the publication (used in the footer message).
            spreadsheet_id (str): The ID of the Google Spreadsheet containing the papers.

        Returns:
            Optional[dict]: The Slack API response on success, or None if there is an error.
        """
        try:
            header = "Good morning :coffee: Here are today's papers! Enjoy your reading! :wave:\n"
            footer = (
                f"*View all papers:* <https://docs.google.com/spreadsheets/d/{spreadsheet_id}|Google Sheet> :books:"
            )
            message_blocks: List[Dict[str, Any]] = [
                {"type": "section", "text": {"type": "mrkdwn", "text": header}},
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*Preprints:*:point_down:"},
                },
            ]
            if preprints:
                for paper in preprints:
                    paper_section = {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": paper},
                    }
                    message_blocks.append(paper_section)
            else:
                message_blocks.append({
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "No preprints found today."},
                })
            message_blocks.append({"type": "divider"})
            message_blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Papers:*:point_down:"},
            })
            if papers:
                for paper in papers:
                    paper_section = {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": paper},
                    }
                    message_blocks.append(paper_section)
            else:
                message_blocks.append({
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "No papers found today."},
                })
            message_blocks.append({"type": "divider"})
            message_blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": footer}})
            message_blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Published on {today}"},
            })
            message_blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Posted with `slack-papers-app` <https://github.com/theislab/slack_papers_bot|GitHub>",
                },
            })
            if not self.channel_id:
                self.logger.error("Channel ID is not provided.")
                return None
            response = self.client.chat_postMessage(
                channel=self.channel_id,
                blocks=message_blocks,
                text=header,
                unfurl_links=False,
                unfurl_media=False,
            )
            self.logger.info(f"Published papers to Slack: {response}")
        except Exception:
            self.logger.exception("Error in publishing papers to Slack: ", exc_info=True)
            return None
        else:
            return response

    def _send_csv(self, papers: pd.DataFrame, root_dir: str, user_id: str, user_query: str) -> Optional[SlackResponse]:
        """
        Sends a CSV file of papers to the specified Slack channel.

        Args:
            papers (pd.DataFrame): The DataFrame containing the papers to be sent.
            root_dir (str): The root directory where the CSV file will be temporarily saved.
            user_id (str): The Slack user ID of the person who requested the CSV.
            user_query (str): The query string used by the user to filter papers.

        Returns:
            Optional[dict]: The Slack API response on success, or None if there is an error.
        """
        csv_path = os.path.join(root_dir, f"{user_id}_requested_papers.csv")
        papers.to_csv(csv_path, index=False)

        try:
            initial_comment = (
                f"Hey <@{user_id}>, here is the CSV file of papers based on your query:\n\n '{user_query}'."
            )

            # Upload the CSV file to Slack
            response = self.client.files_upload(
                channels=self.channel_id,
                file=csv_path,
                title="Requested_Papers",
                initial_comment=initial_comment,
            )

            self.logger.info(f"Successfully uploaded papers CSV to Slack: {response}")

        except Exception:
            # Log any exceptions that occur during the upload
            self.logger.exception("Error encountered while sending CSV file to Slack.", exc_info=True)
            return None
        else:
            return response
        finally:
            # Clean up by removing the CSV file after the upload
            if os.path.exists(csv_path):
                os.remove(csv_path)
