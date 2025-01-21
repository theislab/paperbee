import re
from datetime import datetime
from logging import Logger

from papers.papers_finder import PapersFinder
from slack_bolt import Ack, Respond


def search_articles_command_callback(command, ack: Ack, respond: Respond, logger: Logger, client, context):
    """
    Handles the '/search_articles' command in Slack. Validates the input and searches for papers based on given parameters.
    Args:
        command: The command payload from Slack.
        ack: Function to acknowledge the command.
        respond: Function to send a message back to the user.
        logger: Logger for logging messages.
        client: Slack WebClient for sending messages.
        context: Context object provided by the Bolt framework.
    """
    try:
        user_input = command["text"]
        channel_id = command["channel_id"]
        user_id = command["user_id"]

        # Acknowledge and provide instructions if no input provided
        if not user_input:
            ack(
                "Please format your input as 'query, date' if including a starting date, or just 'query' otherwise."
                "\nQuery must be a list of keywords, enclosed in square brackets and divided by the OR boolean operator"
                "e.g. '[keyword] OR [keyword]...'."
                "\nDate[optional] must be in YYYY-MM-DD format. If not provided, default to the past 24 hours."
                "\n\nExample: [single-cell] OR [sc], 2021-01-01"
            )
            return
        else:
            ack("Received your command! Searching for papers... This might take a while.")

        # Process input
        if "," in user_input:
            parts = user_input.split(",", 1)
            if len(parts) == 2:
                user_query, user_date = parts[0].strip(), parts[1].strip()

                if not is_valid_date(user_date):
                    respond(f"The date must be in YYYY-MM-DD format. You entered: '{user_date}'")
                    return
                user_query, user_query_valid = is_valid_query(user_query)
                if not user_query_valid:
                    respond(f"The query must be in the format '[keyword] OR [keyword]...'. You entered: '{user_query}'")
                    return
                finder = PapersFinder(
                    root_dir="/home/daniele/Code/slack-papers-app/files/",
                    spreadsheet_id="1WV8xjZnUbWpM26nJvs7_fFkh3f2TZuBRdOnI2WUFgEs",
                    sheet_name="Papers",
                    channel_id=channel_id,
                    query=user_query,
                    since=user_date,
                )
                finder.send_csv(user_id, user_query)
            else:
                respond("Format incorrect. Please use the format 'query, date' or 'query' if no date is provided.")
                return
        elif user_input:
            user_query, user_query_valid = is_valid_query(user_input)
            if not user_query_valid:
                respond(f"The query must be in the format '[keyword] OR [keyword]...'. You entered: '{user_input}'")
                return
            finder = PapersFinder(
                root_dir="/home/daniele/Code/slack-papers-app/files/",
                spreadsheet_id="1WV8xjZnUbWpM26nJvs7_fFkh3f2TZuBRdOnI2WUFgEs",
                sheet_name="Papers",
                channel_id=channel_id,
                query=user_query,
            )
            finder.send_csv(user_id, user_query)

        else:
            respond(f"Format incorrect. Use the format 'query,date' or 'query'. You entered: '{user_input}")
            return

    except Exception as e:
        # Log any exceptions that occur and inform the user
        logger.exception("Error processing the search command.", exc_info=True)
        respond(
            f"An error occurred while processing your request.\n{e}\nMost likely the search gave no results.\nPlease try again, expanding your query, or the starting date."
        )


def is_valid_date(date_str):
    """Validate date format and check if it is an actual date."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False
    else:
        return True


def is_valid_query(query):
    query = re.sub(r"\s+OR\s+", " OR ", query.strip())
    parts = query.split(" OR ")
    if all(part.startswith("[") and part.endswith("]") for part in parts):
        valid_structure = all(part.count("[") == 1 and part.count("]") == 1 for part in parts)
        return query, valid_structure
    else:
        return query, False
