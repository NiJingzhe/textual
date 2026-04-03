"""A simple IM chat app example."""

from __future__ import annotations

import random
from datetime import datetime

from textual import on, tailwind_tcss
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Input, RichLog, Static


RESPONSES = [
    "That's interesting! Tell me more.",
    "I see what you mean.",
    "Hmm, let me think about that...",
    "Great point!",
    "Could you elaborate on that?",
    "I agree completely.",
    "That's a good question.",
    "Let's discuss this further.",
    "I appreciate you sharing that.",
    "Sounds good to me!",
]


class ChatApp(App):
    """A simple IM chat application."""

    CSS = (
        tailwind_tcss()
    )

    BINDINGS = [("q", "quit", "Quit")]

    bot_name = "Bot"

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(
            highlight=True,
            wrap=True,
            markup=True,
            id="chat-log",
            classes="h-fr border p-1",
        )
        with Horizontal(id="input-bar", classes="dock-bottom h-auto px-1"):
            yield Input(
                placeholder="Type a message...", id="chat-input", classes="w-fr px-1"
            )
        yield Static(
            "Press Enter to send. Type /quit to exit.",
            id="status-bar",
            classes="dock-bottom h-[1] bg-slate-700 px-1",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.add_message(
            self.bot_name, "Hello! How can I help you today?", is_user=False
        )

    def add_message(self, sender: str, text: str, is_user: bool = True) -> None:
        chat_log = self.query_one("#chat-log", RichLog)
        color = "blue" if is_user else "green"
        timestamp = datetime.now().strftime("%H:%M")
        chat_log.write(
            f"[bold {color}]{sender}[/bold {color}] [dim]{timestamp}[/dim]\n{text}\n"
        )

    @on(Input.Submitted, "#chat-input")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return

        event.input.clear()

        if text.lower() == "/quit":
            self.exit()
            return

        self.add_message("You", text, is_user=True)

        response = random.choice(RESPONSES)
        self.add_message(self.bot_name, response, is_user=False)


if __name__ == "__main__":
    app = ChatApp()
    app.run()
