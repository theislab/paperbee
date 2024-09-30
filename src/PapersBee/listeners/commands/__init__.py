from slack_bolt import App

from .search_articles_command import search_articles_command_callback


def register(app: App):
    app.command("/search-articles")(search_articles_command_callback)
