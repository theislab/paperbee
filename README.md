# Papersbee

<img src="images/papersbee_logo.png" width="200" height="auto" alt="logo"/>

Papersbee is a Python application designed to daily look for new scientific papers and post them. Currently, the following channels are supported:

- Slack
- Google Sheets
- Telegram
- Zulip
- Telegram

## How does it work?

![papersbee_pipeline](images/papersbee_pipeline.svg)

Papersbee queries scientific papers using keywords specified by user from PubMed and preprint services relying on [findpapers](https://github.com/jonatasgrosman/findpapers/) library. Papers are then filtered either manually via a command-line interface or automatically via an LLM. The filtered papers are then posted to a google sheet and, if desired, to slack or telegram channels.

## Installation

### Download the code and install the dependencies

> ```bash
> pip install PapersBee
> ```

### Setup Google Sheets

1. Create a Google Service Account. Follow the oficial documentation [here](https://cloud.google.com/iam/docs/service-accounts-create). It is needed to put found papers in a Google Spreadsheet.
2. Create a JSON key for the service account. Follow the oficial documentation [here](https://cloud.google.com/iam/docs/keys-create-delete) to create a key pair. Download the JSON file with the key and store it in a convenient location on your machine. Also copy the email of the service account somewhere, you'll need it on the step 5.
3. Enable the Google Sheets API for the service account. Go to the [Google Cloud Console](https://console.cloud.google.com/), click on "APIs and Services" and enable the Google Sheets API.
4. Create a Google Spreadsheet. You can simply copy this [template](https://docs.google.com/spreadsheets/d/13QqH13psraWsTG5GJ7jrqA8PkUvP_HlzO90BMxYwzYw/), but if you prefer, you can create your own. It must have the following columns: `DOI`, `Date`, `PostedDate`, `IsPreprint`, `Title`, `Keywords`, `Preprint`, `URL`. The sheet name must be `Papers`.
5. Set the variables `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_SPREADSHEET_ID` in your `.bashrc` file with the path to the JSON key you created and the ID of the spreadsheet you created. ID of the spreadsheet can be found in the URL of the spreadsheet after `d/`. For example, in the template spreadsheet it is `13QqH13psraWsTG5GJ7jrqA8PkUvP_HlzO90BMxYwzYw`.

> ```bash
> export GOOGLE_CREDENTIALS_JSON="/path/to/credentials.json"
> export GOOGLE_SPREADSHEET_ID="your-spreadsheet-id"
> ```

Alternatively, you can simply set these variables in [config](src/PapersBee/papers/config.py).

<div style="background-color: salmon; padding: 10px; border: 1px solid black; border-radius: 5px;">
<b>Important!</b> When setting up variables in config, don't share it with anyone online (e.g. add it to .`gitignore` to not commit accidentally). Loosing your tokens might lead to other people using them for their purposes.
</div>

6. Add the service account email to the spreadsheet. Go to the spreadsheet, click on the three dots in the top right corner, click on *Share*, paste the service account email into the *Add people* field, and give it the *Editor* role.

### Get NCBI API key

Code relies on NCBI API to fetch papers and get DOIs from PubMed. It is free, but you need to get an API key

1. Follow the instructions [here](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys) to get an API key.
2. Set the variable `NCBI_API_KEY` in the in the environment file.

> ```bash
> export NCBI_API_KEY="ncbi key"
> ```

Or, alternatively, set `NCBI_API_KEY` variable in [config.py](src/PapersBee/papers/config.py).

### Setup Posting channels

<div style="background-color: salmon; padding: 10px; border: 1px solid black; border-radius: 5px;">
Setup at least one of the three.
</div>

#### Setup Slack (optional)

1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*. The manifest can be modified any time.
4. Review the configuration and click *Create*
5. Click *Install to Workspace* and *Allow* on the screen that follows. You'll then be redirected to the App Configuration dashboard.
6. Open your apps configuration page from this list, click **OAuth & Permissions** in the left hand menu, then copy the Bot User OAuth Token. Store this in the environment as `SLACK_BOT_TOKEN`.
7. Click ***Basic Information** from the left hand menu and follow the steps in the App-Level Tokens section to create an app-level token with the `connections:write` scope. Store this token in the environment as `SLACK_APP_TOKEN`.
8. Set the variable `SLACK_CHANNEL_ID` in the environment to the ID of the channel you want to post to. It can be found in the settings of the channel.

> ```bash
> export SLACK_CHANNEL_ID="slack channel id where to post"
> export SLACK_APP_TOKEN="the app token"
> export SLACK_BOT_TOKEN="the bot token"
> ```

Or, alternatively, fill out the `SLACK` dictionary in [config.py](src/PapersBee/papers/config.py).

#### Setup Telegram (optional)

1. Create a Telegram bot. Follow the instructions [here](https://core.telegram.org/bots/#how-do-i-create-a-bot).
2. Set the variable `TELEGRAM_BOT_API_KEY` in the environment file.
3. Create a Telegram channel or a group and add the bot to the channel as an administrator with the write permissions.
4. Set the variable `TELEGRAM_CHANNEL_ID` in the environment file.

- To get the ID of the channel, you can use the [@myidbot](https://t.me/myidbot) bot. Just share a message from the channel with the bot and it will reply with the ID of the channel.

> ```bash
> export TELEGRAM_BOT_API_KEY="the bot api key"
> export TELEGRAM_CHANNEL_ID="telegram channel id where to post"
> ```

Or, alternatively, fill out the `TELEGRAM` dictionary in [config.py](src/PapersBee/papers/config.py).

#### Setup Zulip (optional)

1. Create a Zulip bot and download the `zuliprc` file. Follow the instructions [here](https://zulip.com/help/add-a-bot-or-integration).
2. Set the variable `ZULIP_PRC` in your environment to point to the downloaded zuliprc file path.
3. Create a stream (if needed), and suscribe the bot to the stream you want the bot to post papers in.
4. Set `ZULIP_STREAM` and `ZULIP_TOPIC` in your environment.

> ```bash
> export ZULIP_PRC="path to zuliprc"
> export ZULIP_STREAM="zulip stream where to post"
> export ZULIP_TOPIC="zulip topic where to post"
> ```

Or, alternatively, fill out the `ZULIP` dictionary in [config.py](src/PapersBee/papers/config.py).

### Setup LLM for automated filtering (optional, but highly recommended)

<div style="background-color: salmon; padding: 10px; border: 1px solid black; border-radius: 5px;">
If you want to use LLM filtering remember to add a filtering_prompt.txt file. See <a href="#setup-query-and-llm-filtering-prompt">Setup query and LLM filtering prompt</a>.
</div>

#### Setup OpenAI API key

GPT model is used to filter irrelevant papers. You can also do it manually, but LLM is much faster and allows to run bot fully automatically.

0. Register an account on [OpenAI developer platform](https://platform.openai.com/signup)
1. Follow the instructions [here](https://platform.openai.com/settings/organization/api-keys) to get an API key.
2. Set the variable `OPENAI_API_KEY` in in the environment file.
3. Put some money on your account. For the query in this repo, it takes less than $0.01 per day to run.

> ```bash
> export LLM_PROVIDER="openai"
> export OPENAI_API_KEY="api key"
> export LANGUAGE_MODEL="your favorite gpt model"
> ```

Or, alternatively, set these variables in [config.py](src/PapersBee/papers/config.py).

#### Setup Ollama

Open source LLMs can also be used to filter irrelevant papers.

0. Download Ollama on your system [OpenAI developer platform](https://ollama.com/download/)
1. Decide which LLM to use out of the [available ones](https://ollama.com/search), on a terminal run ollama pull <model_name>. We find `llama3.2` to be a good compromise in terms of hardware requirement and performances, but feel free to use your favourite LLM.
2. Set the variable `LANGUAGE_MODEL` with the model name in the environment.

> ```bash
> export LLM_PROVIDER="ollama"
> export LANGUAGE_MODEL="your favorite LLM model"
> ```

Or, alternatively, set these variables in [config.py](src/PapersBee/papers/config.py).

### Setup query and LLM filtering prompt

1. Create an empty directory where to store the query files.
2. Create a query – list of keywords to search papers. You can use this [template](files/query.txt). For syntax instructions, refer to [findpapers documentation](https://github.com/jonatasgrosman/findpapers). Since biorxiv only allows for `OR` boolean operator while pubmed and arxiv also allow for `AND` and `AND NOT` if you want to fine tune your query create two separate files:
   1. `query_biorxiv.txt` for the biorxiv quey where only `OR` is used
   2. `query_pubmed_arxiv.txt` where the other boolean operators can be used.
3. Else only use `query.txt`
4. If using LLM filtering, create a `filtering_prompt.txt` file. Use this [template](files/filtering_prompt.txt)
5. Store the files in the directory you created.
6. Set the variable `LOCAL_ROOT_DIR` in the in the environment pointing to the directory you created.

<div style="background-color: salmon; padding: 10px; border: 1px solid black; border-radius: 5px;">
If query.txt is not present both query_biorxiv.txt and query_pubmed_arxiv.txt must be present
</div>

Make sure that you run it in the correct environment. If everything works, you should see success messages in the terminal, and some messages with and without papers in the test channels.

> ```bash
> export LOCAL_ROOT_DIR="path to the folder where queries and llm prompts are stored"
> ```

Or, alternatively, set the `LOCAL_ROOT_DIR` variable in [config.py](src/PapersBee/papers/config.py).

## Running the bot

When everything is set up, you can simply run the bot with:

> ```bash
> papersbee post --interactive --since 10
> ```

`interactive` is optional, if it is set the LLM settings will be override and the filtering will instead be interactive through the CLI.

`since` is optional, can be used to specify how many days back to search for papers. If not specified the bot will search for papers published in the last 24h.

## Project Structure

### `manifest.json`

`manifest.json` is a configuration for Slack apps. With a manifest, you can create an app with a pre-defined configuration, or adjust the configuration of an existing app.

#### `src/PapersBee/papers`

Classes to fetch the papers, format them, and post them on slack along with updating the papers google sheet.

- `src/PapersBee/papers/utils.py` Preprocessor for `findpapers` output, and to extract DOIs from pubmed.
- `src/PapersBee/papers/google_sheet.py` Class to check and update the papers google sheet.
- `src/PapersBee/papers/llm_filtering.py` Class to filter paper with LLMs
- `src/PapersBee/papers/cli.py` Class to filter paper with interactively in the CLI
- `src/PapersBee/papers/slack_papers_formatter.py` Format the papers and publish them on slack.
- `src/PapersBee/papers/zulip_papers_formatter.py` Format the papers and publish them on zulip.
- `src/PapersBee/papers/telegram_papers_formatter.py` Format the papers and publish them on telegram.
- `src/PapersBee/papers/papers_finder.py` is the main wrapper class.
- `src/PapersBee/daily_posting.py` is the entry point for the CLI command.

### Running tests (optional)

If you enjoyed setting up, you can enjoy a bit more by creating additional test channels for slack and/or telegram. Or you can run the tests in the actual channels. In any case, set the following variables in the [papers/config.py](papers/config.py) file or in environment:

- `TELEGRAM_TEST_CHANNEL_ID` – ID of the slack channel to post to.
- `SLACK_TEST_CHANNEL_ID` – ID of the telegram channel to post to.

Then simply run the tests with:

> ```zsh
> pytest
> ```
