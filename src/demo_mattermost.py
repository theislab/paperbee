import os
import logging
from PaperBee.papers.mattermost_papers_formatter import MattermostPaperPublisher
from tests.sample_papers import sample_papers

# Usage: Set MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_TEAM, MATTERMOST_CHANNEL env vars before running.

# Sample paper data (from tests/test_telegram.py)
# papers_data = [
#     [
#         "10.1101/2024.04.26.591400",
#         "2024-04-29",
#         "2024-04-28",
#         "TRUE",
#         "Single-Cell Transcriptomics Reveals the Molecular Logic Underlying Ca2+ Signaling Diversity in Human and Mouse Brain",
#         "https://doi.org/10.1101/2024.04.26.591400",
#     ],
#     [
#         "10.1101/2024.04.22.590645",
#         "2024-04-29",
#         "2024-04-26",
#         "TRUE",
#         "scMUSCL: Multi-Source Transfer Learning for Clustering scRNA-seq Data",
#         "https://doi.org/10.1101/2024.04.22.590645",
#     ],
#     [
#         "10.1101/2024.04.21.590442",
#         "2024-04-29",
#         "2024-04-26",
#         "TRUE",
#         "Imbalance and Composition Correction Ensemble Learning Framework (ICCELF): A novel framework for automated scRNA-seq cell type annotation",
#         "https://doi.org/10.1101/2024.04.21.590442",
#     ],
# ]

def main():
    logger = logging.getLogger(__name__)
    url = os.environ.get("MATTERMOST_URL")
    token = os.environ.get("MATTERMOST_TOKEN")
    team = os.environ.get("MATTERMOST_TEAM")
    channel = os.environ.get("MATTERMOST_CHANNEL")

    if not all([url, token, team, channel]):
        raise ValueError("Please set MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_TEAM, MATTERMOST_CHANNEL environment variables.")

    publisher = MattermostPaperPublisher(
        logger=logger,
        url=url,
        token=token,
        team=team,
        channel=channel,
    )
    post = publisher.publish_papers(sample_papers)
    print(f"Message sent to Mattermost channel {channel}: {post['id']}")

if __name__ == "__main__":
    main() 