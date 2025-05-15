---
title: 'Papersbee: An Automated Daily Digest Bot for Scientific Literature Monitoring'
tags:
  - python
  - automation
  - scientific literature
  - LLM

authors:
  - name: Daniele Lucarelli
    affiliation: "1,2,3,4"
  - name: Vladimir Shitov
    affiliation: "1"
  - name: Luke Zappia
    affiliation: "1"
  - name: Fabian Theis
    affiliation: "1,5"
    corresponding: true

affiliations:
  - name: "Institute of Computational Biology, Helmholtz Center Munich, Germany."
    index: 1
  - name: "Division of Translational Cancer Research, German Cancer Research Center (DKFZ) and German Cancer Consortium (DKTK), Im Neuenheimer Feld 280, 69120 Heidelberg, Germany"
    index: 2
  - name: "Chair of Translational Cancer Research and Institute of Experimental Cancer Therapy, Klinikum rechts der Isar, TUM School of Medicine and Health, Technical University of Munich, Germany"
    index: 3
  - name: "Center for Translational Cancer Research (TranslaTUM), TUM School of Medicine and Health, Technical University of Munich, Germany"
    index: 4
  - name: "School of Computing, Information and Technology, Technical University of Munich, Munich, Germany."
    index: 5

date: 10 June 2025
bibliography: paper.bib
---

# Summary

Staying current with the ever-expanding body of scientific literature is an increasing challenge for researchers. **Papersbee** is a lightweight, modular, and open-source Python package designed to streamline this process by automating the daily discovery, filtering, and dissemination of new scientific papers, tailored to individual or team research interests. By integrating structured keyword-based queries, access to preprint and PubMed databases via the `findpapers` package [@grosman:2020], and optional filtering powered by large language models (LLMs), Papersbee surfaces relevant papers with minimal manual effort. It further enhances research workflows by posting curated content to team communication platforms such as Slack, Zulip, Telegram, and by maintaining a structured archive in Google Sheets. Papersbee adapts to both interactive and fully automated use cases, enabling individual researchers, labs, and institutions to maintain awareness of cutting-edge developments across multiple domains.

# Statement of Need

The scientific publication landscape is growing at an unprecedented pace, often leaving researchers overwhelmed by the sheer volume of new literature. Conventional alert mechanisms, such as email subscriptions or RSS feeds [@hokamp2004], are limited in scope and flexibility, and fail to integrate with modern collaborative tools. Moreover, they often lack intelligent filtering, leading to low signal-to-noise ratios in alerts. Prior tools with automation capabilities, such as ASReview [@vandeschoot2021], have emphasized systematic review workflows rather than daily monitoring. **Papersbee** fills this gap by offering an open, transparent, and configurable tool tailored for continuous literature monitoring. It bridges automation and collaboration, offering programmable integration with chat platforms and shared spreadsheets, and optional LLM-based semantic filtering that helps surface only the most relevant content.

# Functionality

Papersbee provides a comprehensive suite of features tailored for literature monitoring:

- **Daily Retrieval**: Uses the [findpapers] package [@grosman2020] to access PubMed, arXiv, and bioRxiv through structured keyword queries.
- **Filtering**:
  - Manual CLI interface for hands-on review and selection.
  - Automated relevance filtering using LLMs (OpenAI GPT or open-source alternatives via Ollama) [@dennstaedt2024llm; @cai2025llm], customizable with domain-specific prompts.
- **Multichannel Delivery**: Posts curated papers to Slack, Telegram, and Zulip.
- **Archival**: Automatically logs daily selected papers into Google Sheets for tracking.
- **Configurability**:
  - Modular prompt-based filtering logic for LLMs.
  - Simple configuration for easy setup.

# Implementation

Papersbee adopts a modular architecture that separates core responsibilities into pluggable components: query handling, paper retrieval, filtering, formatting, and publishing. Queries are managed as YAML files and passed to the `findpapers` engine, which interfaces with relevant scientific APIs. The retrieved articles undergo a two-stage filtering process—initially via CLI review or fully automated LLM classification—based on user-defined semantic relevance prompts [@dennstaedt2024llm; @cai2025llm]. Filtered results are formatted into platform-specific message payloads and sent to designated communication channels via their respective APIs. A centralized Google Sheet is used for cumulative archival and collaborative review. This design supports extensibility and interoperability, making it straightforward to plug in new data sources, filters, or output channels.

# Acknowledgements

We gratefully acknowledge the creators and maintainers of the `findpapers` library [@grosman2020], whose work forms the backbone of Papersbee’s retrieval functionality. We also thank the teams behind the PubMed, arXiv, and bioRxiv APIs, which make programmatic literature access possible. Finally, we acknowledge the developers and researchers behind OpenAI and Ollama for the LLMs used in Papersbee's semantic filtering experiments.

# References
