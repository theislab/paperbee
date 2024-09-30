from slack_bolt import App

from .sample_shortcut import sample_shortcut_callback


def register(app: App):
    app.shortcut("sample_shortcut_id")(sample_shortcut_callback)
