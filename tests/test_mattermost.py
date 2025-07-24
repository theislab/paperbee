import pytest
from logging import Logger
from PaperBee.papers.mattermost_papers_formatter import MattermostPaperPublisher

@pytest.fixture
def papers():
    return [
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

@pytest.fixture
def publisher():
    return MattermostPaperPublisher(
        logger=Logger("MattermostTest"),
        channel_id="dummy_channel_id"
    )

def test_format_papers(publisher, papers):
    papers_out, preprints_out = publisher.format_papers(papers)
    assert isinstance(papers_out, list)
    assert isinstance(preprints_out, list)
    # All test data are preprints
    assert len(preprints_out) == len(papers)
    assert all("[" in p and "](" in p for p in preprints_out)

def test_build_message(publisher, papers):
    papers_out, preprints_out = publisher.format_papers(papers)
    message = publisher.build_message(papers_out, preprints_out, today="2024-04-29", spreadsheet_id="dummy_id")
    assert isinstance(message, str)
    assert "Preprints" in message
    assert "Papers" in message
    assert "Good morning" in message 