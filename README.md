# 🐝 PaperBee

<img src="images/paperbee_logo.png" width="200" height="auto" alt="logo"/>

PaperBee is a Python application designed to **automatically search for new scientific papers and post them** to your favorite channels.
Currently supported platforms:

- 🟣 Slack
- 🟢 Zulip
- 🔵 Telegram

---

## 🚀 How Does It Work?

![paperbee_pipeline](images/paperbee_pipeline.svg)

PaperBee queries scientific papers using user-specified keywords from PubMed and preprint services, relying on the [findpapers](https://github.com/jonatasgrosman/findpapers/) library.
Papers are then filtered either **manually via a command-line interface** or **automatically via an LLM**.
The filtered papers are posted to a Google Sheet and, if desired, to Slack, Telegram, or Zulip channels.
PaperBee is easy to setup and configure with a simple `yml` file.

---

## 📦 Installation

### 1. Download the Code and Install Dependencies

```bash
pip install paperbee
```

---

## 📝 Setup Guide

### 1. Google Sheets Integration

1. **Create a Google Service Account:**
   [Official guide](https://cloud.google.com/iam/docs/service-accounts-create)
   Needed to write found papers to a Google Spreadsheet.
2. **Create a JSON Key:**
   [Official guide](https://cloud.google.com/iam/docs/keys-create-delete)
   Download and store the JSON file securely.
3. **Enable Google Sheets API:**
   In [Google Cloud Console](https://console.cloud.google.com/), enable the Google Sheets API for your service account.
4. **Create a Google Spreadsheet:**
   You can copy this [template](https://docs.google.com/spreadsheets/d/13QqH13psraWsTG5GJ7jrqA8PkUvP_HlzO90BMxYwzYw/).
   The sheet must have columns: `DOI`, `Date`, `PostedDate`, `IsPreprint`, `Title`, `Keywords`, `Preprint`, `URL`.
   The sheet name must be `Papers`.
5. **Share the Spreadsheet:**
   Add the service account email as an _Editor_.

---

### 2. 🔑 Get NCBI API Key

PaperBee uses the NCBI API to fetch papers and DOIs from PubMed.
[Get your free API key here.](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys)

---

### 3. 📢 Setup Posting Channels

> **You must set up at least one of the three platforms below.**

#### 🟣 Slack (optional)

1. [Create a Slack App](https://api.slack.com/apps/new) (choose "From an app manifest").
2. Choose your workspace.
3. Copy the contents of `manifest.json` into the manifest box.
4. Review and create the app.
5. Install to Workspace and allow permissions.
6. In **OAuth & Permissions**, copy the Bot User OAuth Token.
7. In **Basic Information**, create an app-level token with `connections:write` scope.
8. Set `SLACK_CHANNEL_ID` to your desired channel's ID.

Update the **SLACK** variables in the `config.yml` file.

#### 🔵 Telegram (optional)

1. Create a Telegram bot [Follow the instructions here](https://core.telegram.org/bots/#how-do-i-create-a-bot).
2. Create a channel or group, add the bot as admin.
3. Use [@myidbot](https://t.me/myidbot) to get the channel ID.

Update the **TELEGRAM** variables in the `config.yml` file.

#### 🟢 Zulip (optional)

1. [Create a Zulip bot](https://zulip.com/help/add-a-bot-or-integration) and download the `zuliprc` file.
2. Create a stream and subscribe the bot.

Update the **ZULIP** variables in the `config.yml` file.

---

### 4. 🤖 Setup LLM for Automated Filtering (optional, but recommended)

> If you want to use LLM filtering, remember to add a `filtering_prompt.txt` file.
> See [Setup Query and LLM Filtering Prompt](#setup-query-and-llm-filtering-prompt).

#### OpenAI API

- [Sign up for OpenAI](https://platform.openai.com/signup)
- [Get your API key](https://platform.openai.com/settings/organization/api-api-keys)
- Add credits to your account.

#### Ollama (Open Source LLMs)

- [Download Ollama](https://ollama.com/download/)
- Pull your preferred model (e.g., `ollama pull llama3.2`).

Update the **LLM** variables in the `config.yml` file. (LLM_PROVIDER, LANGUAGE_MODEL, OPENAI_API_KEY)

---

## ⚙️ Configuration

PaperBee uses a YAML configuration file to specify all arguments.
Copy and customize the template below as `config.yml`:

### Example `config.yml`

```yaml
GOOGLE_SPREADSHEET_ID: "your-google-spreadsheet-id"
GOOGLE_CREDENTIALS_JSON: "/path/to/your/google-credentials.json"
NCBI_API_KEY: "your-ncbi-api-key"

# path to the local root directory where query prompts and files are stored
LOCAL_ROOT_DIR: "/path/to/local/root/dir"

# Queries. You can set either only "query" to use in all databases or query_biorxiv and query_pubmed_arxiv.
# Note that biorxiv only accept OR boolean operator while pubmed and arxiv also accept AND and AND NOT, this is why tje two queries are separated.
# More info: https://github.com/jonatasgrosman/findpapers?tab=readme-ov-file#search-query-construction
query: "[AI for cell trajectories] OR [machine learning for cell trajectories] OR [deep learning for cell trajectories] OR [AI for cell dynamics] OR [machine learning for cell dynamics] OR [deep learning for cell dynamics]"
query_biorxiv: "[AI for cell trajectories] OR [machine learning for cell trajectories] OR [deep learning for cell trajectories] OR [AI for cell dynamics] OR [machine learning for cell dynamics] OR [deep learning for cell dynamics]"
query_pubmed_arxiv: "([single-cell transcriptomics]) AND ([Cell Dynamics]) AND ([AI] OR [machine learning] OR [deep learning]) AND NOT ([proteomics])"

# LLM Filtering (optional)
LLM_FILTERING: true
LLM_PROVIDER: "openai"
LANGUAGE_MODEL: "gpt-4o-mini"
OPENAI_API_KEY: "your-openai-api-key"
# Describe what are your interests and what kind of papers are relevant to your lab.
# Change lab focus and interests to your own. Feel free to add more details and examples, but leave the last sentence as is.
FILTERING_PROMPT: "You are a lab manager at a research lab focusing on machine learning methods development for single-cell RNA sequencing. Lab members are interested in developing methods to model cell dynamics. You are reviewing a list of research papers to determine if they are relevant to your lab. Please answer 'yes' or 'no' to the following question: Is the following research paper relevant?"

# Slack configuration
SLACK:
  is_posting_on: true
  bot_token: "your-slack-bot-token"
  channel_id: "your-slack-channel-id"
  app_token: "your-slack-app-token"

# Telegram configuration
TELEGRAM:
  is_posting_on: true
  bot_token: "your-telegram-bot-token"
  channel_id: "your-telegram-channel-id"

# Zulip configuration
ZULIP:
  is_posting_on: false
  prc: "path-to-your-zulip-prc"
  stream: "your-zulip-stream"
  topic: "your-zulip-topic"

SLACK_TEST_CHANNEL_ID: "your-slack-test-channel-id" # not required so left outside of dictionary
TELEGRAM_TEST_CHANNEL_ID: "your-slack-test-channel-id" # not required so left outside of dictionary
GOOGLE_TEST_SPREADSHEET_ID: "your-google-test-spreadsheet-id" # not required so left outside of dictionary
```

---

### 📄 Example Query and Prompt

#### `query`

If specifying a list of keyword is enough, you can simply fit one query for all databases. Example:

```text
[AI for cell trajectories] OR [machine learning for cell trajectories] OR [deep learning for cell trajectories] OR [AI for cell dynamics] OR [machine learning for cell dynamics] OR [deep learning for cell dynamics]
```

Both Arxiv and Pubmed allow for more refined queries.
If you want to fine-tune the queries for pubmed and arxiv which allow for both AND and AND NOT boolean operators, then you will need to split the queries in two (read below).

#### `query_biorxiv`

This database has more requirements, so if your query is complex, you have to set a separate simple query for biorxiv, and a complex query for everything else. See [findpapers documentation](https://github.com/jonatasgrosman/findpapers?tab=readme-ov-file#search-query-construction) for more details. TLDR:

- Only **1-level grouping** is supported: no round brackets inside round brackets
- **Only OR connectors between parenthesis** are allowed, no `() AND ()`!
- **AND NOT is not allowed**
- All connectors must be either OR or AND. **No mixing**!

Here's an example of a valid query:

```text
[AI for cell trajectories] OR [machine learning for cell trajectories] OR [deep learning for cell trajectories] OR [AI for cell dynamics] OR [machine learning for cell dynamics] OR [deep learning for cell dynamics]
```

#### `query_pubmed_arxiv.txt`

Pubmed and Arxiv don't have such requirements, so query can be more complex:

```text
([single-cell transcriptomics]) AND ([Cell Dynamics]) AND ([AI] OR [machine learning] OR [deep learning]) AND NOT ([proteomics])
```

#### `filtering_prompt`

Simply describe your lab interests, which type of papers you want to see and which you don't. The more details, the better! But always leave the last sentence with the question as is. Here is an example:

```text
You are a lab manager at a research lab focusing on machine learning methods development for single-cell RNA sequencing. Lab members are interested in developing methods to model cell dynamics. You are reviewing a list of research papers to determine if they are relevant to your lab. Please answer 'yes' or 'no' to the following question: Is the following research paper relevant?
```

---

## ▶️ Running the Bot

When everything is set up, run the bot with:

```bash
paperbee post --config /path/to/config.yml --interactive --since 10
```

- `--config` : Path to your YAML configuration file.
- `--interactive` : (Optional) Use CLI for manual filtering.
- `--since` : (Optional) How many days back to search for papers (default: last 24h).
- `--databases`: (Optional) list of databases to search, default pubmed biorxiv

See [daily_posting.py](src/PaperBee/daily_posting.py) for an example of running search from Python.

---

## 🗂️ Project Structure

### `manifest.json`

Configuration for Slack apps.
With a manifest, you can create or adjust an app with a pre-defined configuration.

### `src/PaperBee/papers`

Classes to fetch, format, and post papers, and update the Google Sheet.

- `utils.py` – Preprocess `findpapers` output, extract DOIs.
- `google_sheet.py` – Update/check the Google Sheet.
- `llm_filtering.py` – Filter papers with LLMs.
- `cli.py` – Interactive CLI filtering.
- `slack_papers_formatter.py` – Format and post to Slack.
- `zulip_papers_formatter.py` – Format and post to Zulip.
- `telegram_papers_formatter.py` – Format and post to Telegram.
- `papers_finder.py` – Main wrapper class.
- `daily_posting.py` – CLI entry point.

---

## 🧪 Running Tests (Optional)

You can set up test channels for Slack/Telegram or run tests in production channels.
Set the following variables in your `config.yml`:

- `TELEGRAM_TEST_CHANNEL_ID` – Telegram test channel ID.
- `SLACK_TEST_CHANNEL_ID` – Slack test channel ID.
- `GOOGLE_TEST_SPREADSHEET_ID` – Test spreadsheet ID. **Don't use a production spreadsheet!**

**Install extra dependencies:**

```bash
pip install pytest-asyncio
```

or with Poetry:

```bash
poetry install --with dev
```

**Run the tests:**

```bash
pytest
```

---

# Reference

```
@misc{shitov_patpy_2024,
  author = {Lucarelli, Daniele and Shitov, Vladimir A. and Saur, Dieter and Zappia, Luke and Theis, Fabian J.},
  title = {PaperBee: An Automated Daily Digest Bot for Scientific Literature Monitoring},
  year = {2025},
  url = {https://github.com/theislab/paperbee},
  note = {Version 1.0.0}
}
```

Enjoy using 🐝 **PaperBee**!
