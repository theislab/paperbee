from logging import Logger
from typing import List, Optional, Tuple

from telegram import Bot, Message


def escape_reserved_symbols(text: str, symbols: str = "!.-+>()") -> str:
    """
    Escapes reserved symbols in the given text to be compatible with Telegram's MarkdownV2 format.

    Args:
        text (str): The input text containing symbols that need to be escaped.
        symbols (str): A string of symbols to escape. Defaults to "!.-+>()".

    Returns:
        str: The text with reserved symbols escaped.
    """
    for symbol in symbols:
        text = text.replace(symbol, f"\\{symbol}")
    return text


class TelegramPaperPublisher:
    """
    A class to publish academic papers to a Telegram channel.

    Args:
        logger (Logger): A logger instance for logging information and errors.
        channel_id (str): The Telegram channel ID where papers will be published.
        bot (Bot): A Telegram bot instance used to send messages.
    """

    def __init__(
        self,
        logger: Logger,
        channel_id: Optional[str] = None,
        bot_token: Optional[str] = None,
    ) -> None:
        """
        Initializes the TelegramPaperPublisher with the logger, channel ID, and bot token.

        Args:
            logger (Logger): The logger instance for logging messages.
            channel_id (str): The Telegram channel ID. Defaults to None.
            bot_token (str): The bot token used for authentication. Defaults to None.
        """
        self.logger = logger
        if channel_id:
            self.channel_id = channel_id
        else:
            e = "Channel ID is required to publish papers to Telegram."
            raise ValueError(e)
        if bot_token:
            self.bot = Bot(bot_token)
        else:
            e = "Bot token is required to publish papers to Telegram."
            raise ValueError(e)

    @staticmethod
    def format_papers(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
        """
        Formats a list of papers into separate lists for regular papers and preprints with Telegram MarkdownV2 formatting.

        Args:
            papers_list (List[List[str]]): A list of papers, where each paper is a list of Args.

        Returns:
            Tuple[List[str], List[str]]: Two lists, one for regular papers and one for preprints, each formatted for Telegram.
        """
        papers = []
        preprints = []
        for paper in papers_list:
            emoji = "✏️" if paper[3] == "TRUE" else "🗞️"
            title = escape_reserved_symbols(paper[4])
            link = escape_reserved_symbols(paper[-1])
            formatted_paper = f"{emoji} [{title}]({link})"

            if paper[3] == "TRUE":
                preprints.append(formatted_paper)
            else:
                papers.append(formatted_paper)

        return papers, preprints

    async def publish_papers(
        self,
        papers: List[str],
        preprints: List[str],
        today: str,
        spreadsheet_id: str,
    ) -> Optional[Message]:
        """
        Publishes the formatted papers and preprints to the specified Telegram channel.

        Args:
            papers (List[str]): A list of formatted regular papers.
            preprints (List[str]): A list of formatted preprints.
            today (str): The date for the publication (used in the footer message).
            spreadsheet_id (str): The ID of the Google Spreadsheet containing the papers.

        Returns:
            None
        """
        divider = escape_reserved_symbols("────────────")

        try:
            header = "Good morning ☕ Here are today's papers\\!\n"
            footer = "\nEnjoy your reading\\! 👋\n"
            message_blocks = [header, "*Preprints:*👇"]

            if len(preprints) > 0:
                for paper in preprints:
                    message_blocks.append(paper)
            else:
                message_blocks.append("No preprints found today\\.")

            message_blocks.append(divider)
            message_blocks.append("\n*Papers:*👇")

            if len(papers) > 0:
                for paper in papers:
                    message_blocks.append(paper)
            else:
                message_blocks.append("No papers found today\\.")

            message_blocks.append(divider)
            message_blocks.append(footer)

            response = await self.bot.send_message(
                chat_id=self.channel_id,
                text="\n".join(message_blocks),
                parse_mode="MarkdownV2",
            )
            self.logger.info(f"Published papers to Telegram: {response}")
        except Exception:
            self.logger.exception("Error in publishing papers to Telegram: ", exc_info=True)
        else:
            return response

        return None
