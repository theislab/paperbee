from logging import Logger
from slack_sdk import WebClient
from typing import List, Tuple, Any
import pandas as pd
import os


class SlackPaperPublisher:
    def __init__(
        self, client: WebClient, logger: Logger, channel_id: str = None
    ):
        self.client = client
        self.logger = logger
        self.channel_id = channel_id

    @staticmethod
    def format_papers_for_slack(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
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
        papers: List[List[str]],
        preprints: List[List[str]],
        today: str,
        spreadsheet_id: str,
    ) -> None:
        try:
            header = "Good morning :coffee: Here are today's papers! Enjoy your reading! :wave:\n"
            footer = f"*View all papers:* <https://docs.google.com/spreadsheets/d/{spreadsheet_id}|Google Sheet> :books:"
            message_blocks = [
                {"type": "section", "text": {"type": "mrkdwn", "text": header}},
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Preprints:*:point_down:"},
                },
            ]
            if len(preprints) > 0:
                for paper in preprints:
                    paper_section = {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": paper},
                    }
                    message_blocks.append(paper_section)
            else:
                message_blocks.append(
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "No preprints found today."},
                    }
                )
            message_blocks.append({"type": "divider"})
            message_blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*Papers:*:point_down:"},
                }
            )
            if len(papers) > 0:
                for paper in papers:
                    paper_section = {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": paper},
                    }
                    message_blocks.append(paper_section)
            else:
                message_blocks.append(
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "No papers found today."},
                    }
                )
            message_blocks.append({"type": "divider"})
            message_blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": footer}}
            )
            message_blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Published on {today}"},
                }
            )
            message_blocks.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Posted with `slack-papers-app` <https://github.com/theislab/slack_papers_bot|GitHub>"}
                }
            )

            response = self.client.chat_postMessage(
                channel=self.channel_id,
                blocks=message_blocks,
                text=header,
                unfurl_links=False,
                unfurl_media=False,
            )
            self.logger.info(f"Published papers to Slack: {response}")
            return response
        except Exception as e:
            self.logger.error("Error in publishing papers to Slack: ", exc_info=True)

    def _send_csv(
        self,
        papers: pd.DataFrame,
        root_dir: str,
        user_id: str,
        user_query: str
    ) -> None:        
        csv_path = os.path.join(root_dir, f"{user_id}_requested_papers.csv")
        papers.to_csv(csv_path, index=False)

        try:
            initial_comment = f"Hey <@{user_id}>, here is the CSV file of papers based on your query:\n\n '{user_query}'."

            # Upload the CSV file to Slack
            response = self.client.files_upload(
                channels=self.channel_id,
                file=csv_path,
                title=f"Requested_Papers",
                initial_comment=initial_comment,
            )

            self.logger.info(f"Successfully uploaded papers CSV to Slack: {response}")
            return response
        
        except Exception as e:
            # Log any exceptions that occur during the upload
            self.logger.error(
                "Error encountered while sending CSV file to Slack.", exc_info=True
            )
        finally:
            # Clean up by removing the CSV file after the upload
            if os.path.exists(csv_path):
                os.remove(csv_path)
