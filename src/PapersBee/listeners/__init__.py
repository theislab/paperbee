from typing import Any

from listeners import actions, commands, events, messages, shortcuts, views


def register_listeners(app: Any) -> None:
    actions.register(app)
    commands.register(app)
    events.register(app)
    messages.register(app)
    shortcuts.register(app)
    views.register(app)
