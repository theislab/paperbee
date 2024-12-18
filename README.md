# Papersbee

Papersbee is a Python application designed to daily look for new scientific papers and post them. Currently, the following channels are supported:
- Slack
- Google Sheets
- Telegram

## Installation

### Download the code and install the dependencies

```zsh
git clone <this repo link>
# From the root directory of the repo
pip install -r requirements.txt
```

### Setup Google Sheets

1. Create a Google Service Account. Follow the oficial documentation [here](https://cloud.google.com/iam/docs/service-accounts-create). It is needed to put found papers in a Google Spreadsheet.
2. Create a JSON key for the service account. Follow the oficial documentation [here](https://cloud.google.com/iam/docs/keys-create-delete) to create a key pair. Download the JSON file with the key and store it in a convenient location on your machine.
3. Create a Google Spreadsheet. You can simply copy this [template](https://docs.google.com/spreadsheets/d/13QqH13psraWsTG5GJ7jrqA8PkUvP_HlzO90BMxYwzYw/), but if you prefer, you can create your own. It must have the following columns: `DOI`, `Date`, `PostedDate`, `IsPreprint`, `Title`, `Keywords`, `Preprint`, `URL`. The sheet name must be `Papers`.
4. Set the variables `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_SPREADSHEET_ID` in the [papers/config.py](papers/config.py) file to the path to the JSON key you created and the ID of the spreadsheet you created. ID of the spreadsheet can be found in the URL of the spreadsheet after `d/`. For example, in the template spreadsheet it is `13QqH13psraWsTG5GJ7jrqA8PkUvP_HlzO90BMxYwzYw`.

> 💡 **Alternative Setup**: Instead of using the config file, you can set these environment variables directly in your system:
> ```bash
> export GOOGLE_CREDENTIALS_JSON="/path/to/credentials.json"
> export GOOGLE_SPREADSHEET_ID="your-spreadsheet-id"
> ```

### Get NCBI API key

Code relies on NCBI API to fetch papers and get DOIs from PubMed. It is free, but you need to get an API key

1. Follow the instructions [here](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys) to get an API key.
2. Set the variable `NCBI_API_KEY` in the [papers/config.py](papers/config.py) file or in environment to the API key you got.

### Setup Slack (optional)

#### Create a Slack App
1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*. The manifest can be modified any time.
4. Review the configuration and click *Create*
5. Click *Install to Workspace* and *Allow* on the screen that follows. You'll then be redirected to the App Configuration dashboard.
6. Open your apps configuration page from this list, click **OAuth & Permissions** in the left hand menu, then copy the Bot User OAuth Token. Store this in [papers/config.py](papers/config.py) or in environment as `SLACK_BOT_TOKEN`.
7. Click ***Basic Information** from the left hand menu and follow the steps in the App-Level Tokens section to create an app-level token with the `connections:write` scope. Store this token in [papers/config.py](papers/config.py) or in environment as `SLACK_APP_TOKEN`.
8. Set the variable `SLACK_CHANNEL_ID` in the [papers/config.py](papers/config.py) file or in environment to the ID of the channel you want to post to. It can be found in the settings of the channel.

### Setup Telegram (optional)

1. Create a Telegram bot. Follow the instructions [here](https://core.telegram.org/bots/#how-do-i-create-a-bot).
2. Set the variable `TELEGRAM_BOT_API_KEY` in the [papers/config.py](papers/config.py) file or in environment to the API key of the bot you created.
3. Create a Telegram channel or a group and add the bot to the channel as an administrator with the write permissions.
4. Set the variable `TELEGRAM_CHANNEL_ID` in the [papers/config.py](papers/config.py) file or in environment to the ID of the channel.
- To get the ID of the channel, you can use the [@myidbot](https://t.me/myidbot) bot. Just share a message from the channel with the bot and it will reply with the ID of the channel.

### Setup OpenAI API key (optional, but highly recommended)

GPT model is used to filter irrelevant papers. You can also do it manually, but LLM is much faster and allows to run bot fully automatically.

0. Register an account on [OpenAI developer platform](https://platform.openai.com/signup)
1. Follow the instructions [here](https://platform.openai.com/settings/organization/api-keys) to get an API key.
2. Set the variable `OPENAI_API_KEY` in the [papers/config.py](papers/config.py) file or in environment to the API key you got.
3. Put some money on your account. For the query in this repo, it takes less than $0.01 per day to run. 

### Setup query and filtering prompt.

1. Create a query – list of keywords to search papers. You can use this [template](files/query.txt). For syntax instructions, refer to [findpapers documentation](https://github.com/jonatasgrosman/findpapers).
2. Set the variable `LOCAL_QUERY_PATH` in the [papers/config.py](papers/config.py) file or in environment to the path to the query you created.
3. Create a filtering prompt. It is a text file with the instructions in natural language for the LLM to filter out irrelevant papers. You can use this [template](files/filtering_prompt.txt).
4. Set the variable `LOCAL_FILTERING_PROMPT_PATH` in the [papers/config.py](papers/config.py) file or in environment to the path to the filtering prompt you created.

### Running tests (optional)

If you enjoyed setting up, you can enjoy a bit more by creating additional test channels for slack and/or telegram. Or you can run the tests in the actual channels. In any case, set the following variables in the [papers/config.py](papers/config.py) file or in environment:
- `TELEGRAM_TEST_CHANNEL_ID` – ID of the slack channel to post to.
- `SLACK_TEST_CHANNEL_ID` – ID of the telegram channel to post to.

Then simply run the tests with:

```zsh
pytest
```

Make sure that you run it in the correct environment. If everything works, you should see success messages in the terminal, and some messages with and without papers in the test channels.

## Running the bot



## Project Structure

### `manifest.json`

`manifest.json` is a configuration for Slack apps. With a manifest, you can create an app with a pre-defined configuration, or adjust the configuration of an existing app.

### Interactive

The code for the interactive part, manages interaction between the users in slack and the app.

#### `app.py`

`app.py` is the entry point for the application and is the file you'll run to start the server. This project aims to keep this file as thin as possible, primarily using it as a way to route inbound requests.

#### `/listeners`

Every incoming request is routed to a "listener". Inside this directory, we group each listener based on the Slack Platform feature used, so `/listeners/shortcuts` handles incoming [Shortcuts](https://api.slack.com/interactivity/shortcuts) requests, `/listeners/views` handles [View submissions](https://api.slack.com/reference/interaction-payloads/views#view_submission) and so on.


### Daily posting

The code for the automated daily posting manages the scheduled daily posting.

#### `daily_posting.py`

Main entry point to start the daily posting routine. If used with schedulers such as cron for linux to automate the posting, set `interactive=False` when initialising the `PapersFinder` class.

#### `/papers`

Classes to fetch the papers, format them, and post them on slack along with updating the papers google sheet.

`/papers/utils/` Preprocessor for `findpapers` output, and to extract DOIs from pubmed.

`/papers/google_sheet/` Class to check and update the papers google sheet.

`/papers/slack_papers_formatter/` Format the papers and publish them on slack. Select the channel the papers will be published from here.

`/papers/papers_finder/` is tha main wrapper class.




## App Distribution / OAuth

Only implement OAuth if you plan to distribute your application across multiple workspaces. A separate `app_oauth.py` file can be found with relevant OAuth settings.

When using OAuth, Slack requires a public URL where it can send requests. In this template app, we've used [`ngrok`](https://ngrok.com/download). Checkout [this guide](https://ngrok.com/docs#getting-started-expose) for setting it up.

Start `ngrok` to access the app on an external network and create a redirect URL for OAuth. 

```
ngrok http 3000
```

This output should include a forwarding address for `http` and `https` (we'll use `https`). It should look something like the following:

```
Forwarding   https://3cb89939.ngrok.io -> http://localhost:3000
```

Navigate to **OAuth & Permissions** in your app configuration and click **Add a Redirect URL**. The redirect URL should be set to your `ngrok` forwarding address with the `slack/oauth_redirect` path appended. For example:

```
https://3cb89939.ngrok.io/slack/oauth_redirect
```

Created with [bolt-python template](https://github.com/slack-samples/bolt-python-starter-template.git)
