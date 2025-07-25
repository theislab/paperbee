import pytest
import logging
from PaperBee.papers.mattermost_papers_formatter import MattermostPaperPublisher
from tests.sample_papers import sample_papers
from unittest.mock import MagicMock
import yaml
import os

@pytest.fixture
def papers():
    return sample_papers

@pytest.fixture
def config():
    config_path = os.environ.get("PAPERBEE_CONFIG", "files/config_template.yml")
    with open(config_path) as f:
        return yaml.safe_load(f)

def test_format_papers(papers):
    papers_out, preprints_out = MattermostPaperPublisher.format_papers(papers)
    assert isinstance(papers_out, list)
    assert isinstance(preprints_out, list)
    assert len(preprints_out) == len(papers)
    assert all("[" in p and "](" in p for p in preprints_out)

def test_build_message(papers):
    publisher = MattermostPaperPublisher(
        logger=logging.getLogger(__name__),
        url="dummy", token="dummy", team="dummy", channel="dummy", driver=MagicMock()
    )
    papers_out, preprints_out = publisher.format_papers(papers)
    message = publisher.build_message(papers_out, preprints_out)
    assert isinstance(message, str)
    assert "Preprints" in message
    assert "Papers" in message
    assert "Good morning" in message

def test_publish_papers(config, papers):
    mm_cfg = config["MATTERMOST"]
    # Only run this test if the config is not using placeholder values
    if "your-mattermost-url" in mm_cfg["url"] or "your-mattermost-access-token" in mm_cfg["token"]:
        pytest.skip("Mattermost config is not set up for integration test.")
    publisher = MattermostPaperPublisher(
        logger=logging.getLogger(__name__),
        url=mm_cfg["url"],
        token=mm_cfg["token"],
        team=mm_cfg["team"],
        channel=mm_cfg["channel"],
    )
    post = publisher.publish_papers(papers)
    assert "id" in post 