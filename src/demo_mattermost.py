import os
from logging import Logger
from PaperBee.papers.mattermost_papers_formatter import MattermostPaperPublisher
from mattermostdriver import Driver

# Usage: Set MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_TEAM, MATTERMOST_CHANNEL env vars before running.

# Sample paper data (from tests/test_telegram.py)
papers_data = [
    [
        "10.1101/2024.04.26.591400",
        "2024-04-29",
        "2024-04-28",
        "TRUE",
        "Single-Cell Transcriptomics Reveals the Molecular Logic Underlying Ca2+ Signaling Diversity in Human and Mouse Brain",
        "https://doi.org/10.1101/2024.04.26.591400",
    ],
    [
        "10.1101/2024.04.22.590645",
        "2024-04-29",
        "2024-04-26",
        "TRUE",
        "scMUSCL: Multi-Source Transfer Learning for Clustering scRNA-seq Data",
        "https://doi.org/10.1101/2024.04.22.590645",
    ],
    [
        "10.1101/2024.04.21.590442",
        "2024-04-29",
        "2024-04-26",
        "TRUE",
        "Imbalance and Composition Correction Ensemble Learning Framework (ICCELF): A novel framework for automated scRNA-seq cell type annotation",
        "https://doi.org/10.1101/2024.04.21.590442",
    ],
]

def main():
    logger = Logger("MattermostTest")
    channel_name = os.environ.get("MATTERMOST_CHANNEL")
    team_name = os.environ.get("MATTERMOST_TEAM")
    url = os.environ.get("MATTERMOST_URL")
    token = os.environ.get("MATTERMOST_TOKEN")

    if not all([channel_name, team_name, url, token]):
        raise ValueError("Please set MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_TEAM, MATTERMOST_CHANNEL environment variables.")

    # Initialize Mattermost driver
    driver = Driver({
        'url': url,
        'token': token,
        'scheme': 'https',
        'port': 443,
        'verify': True,
        'debug': False,
    })
    driver.login()

    # Get team and channel IDs
    team = driver.teams.get_team_by_name(team_name)
    team_id = team['id']
    channel = driver.channels.get_channel_by_name(team_id, channel_name)
    channel_id = channel['id']

    # Format message
    publisher = MattermostPaperPublisher(logger=logger, channel_id=channel_id)
    papers, preprints = publisher.format_papers(papers_data)
    message = publisher.build_message(papers, preprints, today=None, spreadsheet_id=None)

    # Send message
    post = driver.posts.create_post({
        'channel_id': channel_id,
        'message': message
    })
    print(f"Message sent to Mattermost channel {channel_name}: {post['id']}")

if __name__ == "__main__":
    main() 