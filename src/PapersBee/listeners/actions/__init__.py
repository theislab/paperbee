from slack_bolt import App

from .sample_action import sample_action_callback


def register(app: App):
    app.action("sample_action_id")(sample_action_callback)
