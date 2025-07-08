from datetime import date
from tempfile import TemporaryDirectory

import pytest
import yaml
from PaperBee.papers.google_sheet import GoogleSheetsUpdater
from PaperBee.papers.papers_finder import PapersFinder


@pytest.mark.asyncio
async def test_posting():
    with open("files/config.yml") as f:
        config = yaml.safe_load(f)

    # Clean up test google spreadsheet
    gsheet_updater = GoogleSheetsUpdater(
        spreadsheet_id=config.get("GOOGLE_TEST_SPREADSHEET_ID"),
        credentials_json_path=config.get("GOOGLE_CREDENTIALS_JSON"),
    )
    sheet, n_rows = gsheet_updater.open_sheet("Papers")
    if n_rows > 1:
        sheet.delete_rows(2, n_rows + 1)  # Delete all rows except the header, row count starts from 1

    query = "[single-cell transcriptomics] OR [single-cell gene expression] OR [single-cell multiomics] OR [single-cell proteomics] OR [single-cell genomics] OR [single-cell RNA-seq] OR [scRNA] OR [scRNA-seq] OR [single-cell sequencing] OR [spatial transcriptomics] OR [single-nucleus sequencing] OR [snRNA-seq] OR [single-cell transcriptome] OR [single-cell omics]"
    filtering_prompt = "You are a lab manager at a research lab focusing on single-cell RNA sequencing, spatial transcriptomics, machine learning applications and methods development in computational biology. Lab research focuses on fibrosis, VEO-IBD, lung health, COPD, and translational applications of single-cell data. Lab members are interested in building single-cell atlases, working with single-cell data on the level of patients (donors, individuals) and keeping updated on the most recent methods in single-cell biology. Another focus of the lab is benchmarking single-cell analysis tools. A specific area of interest is single-cell data integration. You are reviewing a list of research papers to determine if they are relevant to your lab. Please answer 'yes' or 'no' to the following question: Is the following research paper relevant?"

    with TemporaryDirectory() as temp_dir:
        finder = PapersFinder(
            root_dir=temp_dir,
            spreadsheet_id=config.get("GOOGLE_TEST_SPREADSHEET_ID"),
            sheet_name="Papers",
            llm_filtering=True,
            llm_provider=config.get("LLM_PROVIDER"),
            model=config.get("LANGUAGE_MODEL"),
            OPENAI_API_KEY=config.get("OPENAI_API_KEY"),
            filtering_prompt=filtering_prompt,
            interactive=False,
            slack_bot_token=config.get("SLACK")["bot_token"],
            slack_channel_id=config.get("SLACK_TEST_CHANNEL_ID"),
            telegram_bot_token=config.get("TELEGRAM")["bot_token"],
            telegram_channel_id=config.get("TELEGRAM_TEST_CHANNEL_ID"),
            query=query,
            query_biorxiv=query,
            query_pubmed_arxiv=query,
            google_credentials_json=config.get("GOOGLE_CREDENTIALS_JSON"),
            ncbi_api_key=config.get("NCBI_API_KEY"),
        )

        finder.since = date(2023, 10, 8)
        finder.until = date(2023, 10, 10)

        papers, _, _, _ = await finder.run_daily(post_to_slack=True, post_to_telegram=True)

        assert len(papers) > 3

        # Check scpoli paper
        for paper in papers:
            if paper[4].startswith("Population-level integration of single-cell"):
                break
        else:
            e = "scpoli paper not found"
            raise ValueError(e)

        print(papers)
