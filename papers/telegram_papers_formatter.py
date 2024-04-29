from logging import Logger
from typing import List, Tuple
from telegram import Bot


class TelegramPaperPublisher:
    def __init__(
        self, logger: Logger, channel_id: str = None, bot_token: str = None
    ):
        self.logger = logger
        self.channel_id = channel_id
        self.bot = Bot(bot_token)

    @staticmethod
    def format_papers(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
        papers = []
        preprints = []
        for paper in papers_list:
            emoji = "✏️" if paper[3] == "TRUE" else "🗞️"
            formatted_paper = f"{emoji} <{paper[-1]}|{paper[4]}>"
            if paper[3] == "TRUE":
                preprints.append(formatted_paper)
            else:
                papers.append(formatted_paper)

        return papers, preprints

    def publish_papers(
        self,
        papers: List[List[str]],
        preprints: List[List[str]],
        today: str,
        spreadsheet_id: str,
    ) -> None:
        divider = "────────────"

        try:
            header = "Good morning ☕ Here are today's papers! Enjoy your reading! 👋\n"
            footer = f"*View all papers:* <https://docs.google.com/spreadsheets/d/{spreadsheet_id}|Google Sheet> :books:"
            message_blocks = [
                header,
                "*Preprints:*👇"
            ]
            if len(preprints) > 0:
                for paper in preprints:
                    message_blocks.append(paper)
            else:
                message_blocks.append("No preprints found today.")

            message_blocks.append(divider)
            message_blocks.append("*Papers:*👇")

            if len(papers) > 0:
                for paper in papers:
                    message_blocks.append(paper)
            else:
                message_blocks.append("No papers found today.")

            message_blocks.append(divider)
            message_blocks.append(footer)
            message_blocks.append(f"Published on {today}")
            message_blocks.append("Posted with `slack-papers-app` <https://github.com/lueckenlab/slack_papers_bot|GitHub>")

            response = self.bot.sendMessage(
                chat_id=self.channel_id,
                text=header + "".join(message_blocks),
            )

            self.logger.info(f"Published papers to Telegram: {response}")

            return response
        
        except Exception as e:
            self.logger.error("Error in publishing papers to Telegram: ", exc_info=True)
