from slack_bolt import App

from .sample_view import sample_view_callback


def register(app: App):
    app.view("sample_view_id")(sample_view_callback)
