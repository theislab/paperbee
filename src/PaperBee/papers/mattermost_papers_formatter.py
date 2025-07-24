from logging import Logger
from typing import List, Optional, Tuple

class MattermostPaperPublisher:
    """
    A class to format academic papers for Mattermost channels.

    Args:
        logger (Logger): A logger instance for logging information and errors.
        channel_id (str): The Mattermost channel ID where papers will be published.
    """

    def __init__(
        self,
        logger: Logger,
        channel_id: Optional[str] = None,
    ) -> None:
        """
        Initializes the MattermostPaperPublisher with the logger and channel ID.

        Args:
            logger (Logger): The logger instance for logging messages.
            channel_id (str): The Mattermost channel ID. Defaults to None.
        """
        self.logger = logger
        if channel_id:
            self.channel_id = channel_id
        else:
            e = "Channel ID is required to publish papers to Mattermost."
            raise ValueError(e)

    @staticmethod
    def format_papers(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
        """
        Formats a list of papers into separate lists for regular papers and preprints for Mattermost.

        Args:
            papers_list (List[List[str]]): A list of papers, where each paper is a list of Args.

        Returns:
            Tuple[List[str], List[str]]: Two lists, one for regular papers and one for preprints, each formatted for Mattermost.
        """
        papers = []
        preprints = []
        for paper in papers_list:
            emoji = "✏️" if paper[3] == "TRUE" else "🗞️"
            title = paper[4]
            link = paper[-1]
            formatted_paper = f"{emoji} [{title}]({link})"

            if paper[3] == "TRUE":
                preprints.append(formatted_paper)
            else:
                papers.append(formatted_paper)

        return papers, preprints

    def build_message(
        self,
        papers: List[str],
        preprints: List[str],
        today: str,
        spreadsheet_id: str,
    ) -> str:
        """
        Builds the message to be sent to Mattermost channel.

        Args:
            papers (List[str]): A list of formatted regular papers.
            preprints (List[str]): A list of formatted preprints.
            today (str): The date for the publication (used in the header).
            spreadsheet_id (str): The ID of the Google Spreadsheet containing the papers.

        Returns:
            str: The complete message to send to Mattermost.
        """
        divider = "────────────"
        header = f"Good morning :coffee: Here are today's papers!\n"
        footer = "\nEnjoy your reading! :wave:\n"
        message_blocks = [header, "**Preprints:** :point_down:"]

        if len(preprints) > 0:
            message_blocks.extend(preprints)
        else:
            message_blocks.append("No preprints found today.")

        message_blocks.append(divider)
        message_blocks.append("\n**Papers:** :point_down:")

        if len(papers) > 0:
            message_blocks.extend(papers)
        else:
            message_blocks.append("No papers found today.")

        message_blocks.append(divider)
        message_blocks.append(footer)

        return "\n".join(message_blocks) 