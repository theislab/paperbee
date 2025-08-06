from logging import Logger
from typing import Any, List, Optional, Tuple

from mattermostdriver import Driver


class MattermostPaperPublisher:
    """
    Formats and publishes academic papers to a Mattermost channel.
    Handles all Mattermost API logic and message formatting.
    """

    def __init__(
        self,
        logger: Logger,
        url: str,
        token: str,
        team: str,
        channel: str,
        driver: Optional[Any] = None,
    ) -> None:
        """
        Args:
            logger: Logger instance for logging.
            url: Mattermost server URL.
            token: Mattermost personal access token.
            team: Mattermost team name.
            channel: Mattermost channel name.
            driver: (Optional) Pre-initialized Mattermost driver (for testing/mocking).
        """
        self.logger = logger
        self.url = url
        self.token = token
        self.team = team
        self.channel = channel
        if driver is not None:
            self.driver = driver
        else:
            self.driver = Driver({
                "url": self.url,
                "token": self.token,
                "scheme": "https",
                "port": 443,
                "verify": True,
                "debug": False,
            })
            self.driver.login()
        try:
            team_obj = self.driver.teams.get_team_by_name(self.team)
            self.team_id = team_obj["id"]
        except Exception as e:
            raise RuntimeError(f"Could not find Mattermost team '{self.team}'") from e  # noqa: TRY003
        try:
            channel_obj = self.driver.channels.get_channel_by_name(self.team_id, self.channel)
            self.channel_id = channel_obj["id"]
        except Exception as e:
            raise RuntimeError(f"Could not find Mattermost channel '{self.channel}' in team '{self.team}'") from e  # noqa: TRY003

    @staticmethod
    def format_papers(
        papers_list: List[List[str]],
    ) -> Tuple[List[str], List[str]]:
        """
        Splits and formats papers into preprints and regular papers for Mattermost.
        Args:
            papers_list: List of paper records.
        Returns:
            Tuple of (papers, preprints) as formatted strings.
        """
        papers = []
        preprints = []
        for idx, paper in enumerate(papers_list):
            if not isinstance(paper, list) or len(paper) < 6:
                print(f"Warning: Skipping invalid paper at index {idx}: {paper}")
                continue
            emoji = "✏️" if paper[3] == "TRUE" else "🗞️"
            title = paper[4]
            link = paper[-1]
            if not isinstance(title, str) or not isinstance(link, str):
                print(f"Warning: Skipping paper with invalid title or link at index {idx}: {paper}")
                continue
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
    ) -> str:
        """
        Builds the full message for Mattermost.
        Args:
            papers: List of formatted regular papers.
            preprints: List of formatted preprints.
        Returns:
            The complete message string.
        """
        divider = "────────────"
        header = "Good morning ☕ Here are today's papers!\n"
        footer = "\nEnjoy your reading! 👋\n"
        message_blocks = [header, "**Preprints:** 👇"]
        if preprints:
            message_blocks.extend(preprints)
        else:
            message_blocks.append("No preprints found today.")
        message_blocks.append(divider)
        message_blocks.append("\n**Papers:** 👇")
        if papers:
            message_blocks.extend(papers)
        else:
            message_blocks.append("No papers found today.")
        message_blocks.append(divider)
        message_blocks.append(footer)
        return "\n".join(message_blocks)

    async def publish_papers(self, papers_list: List[List[str]]) -> Any:
        """
        Formats and posts the message to Mattermost.
        Args:
            papers_list: List of paper records.
        Returns:
            The Mattermost API response for the post.
        """
        papers, preprints = self.format_papers(papers_list)
        message = self.build_message(papers, preprints)
        try:
            post = self.driver.posts.create_post({"channel_id": self.channel_id, "message": message})
        except Exception as e:
            raise RuntimeError("Failed to create Mattermost post") from e  # noqa: TRY003
        self.logger.info(f"Message sent to Mattermost channel {self.channel}: {post['id']}")
        return post
