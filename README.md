# SlackPapers

SlackPapers is a Python package designed to post new papers of the day on a Slack channel. 
Created with [https://github.com/slack-samples/bolt-python-starter-template.git](bolt-python template)

## Installation

#### Create a Slack App
1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*. The manifest can be modified any time.
4. Review the configuration and click *Create*
5. Click *Install to Workspace* and *Allow* on the screen that follows. You'll then be redirected to the App Configuration dashboard.

#### Environment Variables
Before you can run the app, you'll need to store some environment variables.

1. Open your apps configuration page from this list, click **OAuth & Permissions** in the left hand menu, then copy the Bot User OAuth Token. You will store this in your environment as `SLACK_BOT_TOKEN`.
2. Click ***Basic Information** from the left hand menu and follow the steps in the App-Level Tokens section to create an app-level token with the `connections:write` scope. Copy this token. You will store this in your environment as `SLACK_APP_TOKEN`.

```zsh
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_APP_TOKEN=<your-app-token>
```

### Setup Your Local Project
```zsh

# Setup conda environment

conda create --name myenv python=3.10

conda activate myenv

# Install dependencies

pip install -r requirements.txt

# Start your local server
python3 app.py
```

#### Linting
```zsh
# Run flake8 from root directory for linting
flake8 *.py && flake8 listeners/

# Run black from root directory for code formatting
black .
```

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
