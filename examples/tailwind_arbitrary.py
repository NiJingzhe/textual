"""Show transparent arbitrary utility classes on widgets.

This example imports the bundled ``tailwind.tcss`` utility sheet for a lean
set of common helpers, then adds arbitrary-value utilities directly in
``classes``.
"""

from textual import on, tailwind_tcss
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Label, Static


class TailwindArbitraryApp(App[None]):
    CSS = (
        tailwind_tcss()
        + """
    Screen {
        align: center middle;
        background: #020617;
    }

    #demo {
        layout: vertical;
        width: 76;
        height: auto;
    }

    #controls {
        height: auto;
        margin-top: 1;
    }

    Button {
        margin-right: 1;
    }
    """
    )

    def compose(self) -> ComposeResult:
        with Container(
            id="demo",
            classes="border-round bg-[#0f172a] px-4 py-2 w-[72]",
        ):
            yield Label(
                "Transparent arbitrary utility classes",
                classes="text-center text-[#f8fafc] bg-[#1e293b] px-2 py-1 border-round",
            )
            yield Label(
                'These are written directly on the widget: classes="w-[42] bg-[#334155] text-[#f8fafc]"',
                classes="text-[#cbd5e1] px-1 py-1",
                markup=False,
            )
            yield Static(
                'classes="w-[42] bg-[#334155] text-[#f8fafc] px-2 py-1 border-round hover:opacity-[40%]"',
                id="sample",
                classes="w-[42] bg-[#334155] text-[#f8fafc] px-2 py-1 border-round hover:opacity-[40%]",
                markup=False,
            )
            yield Static(
                "Toggle the button below to add and remove translate-x-[-4] and opacity-[55%] at runtime.",
                id="motion",
                classes="bg-[#172554] text-[#dbeafe] px-2 py-1 border-round",
                markup=False,
            )
            with Horizontal(id="controls"):
                yield Button(
                    "Toggle motion",
                    id="toggle-motion",
                    classes="w-[18] bg-[#1d4ed8] text-[#eff6ff]",
                )
                yield Button(
                    "Flip palette",
                    id="flip-palette",
                    classes="w-[18] bg-[#047857] text-[#ecfdf5]",
                )
            yield Static(
                "Palette target: bg-[#3f3f46] text-[#fafafa]",
                id="palette",
                classes="w-[30] bg-[#3f3f46] text-[#fafafa] px-2 py-1 border-round",
                markup=False,
            )

    @on(Button.Pressed, "#toggle-motion")
    def toggle_motion(self) -> None:
        self.query_one("#motion", Static).toggle_class(
            "translate-x-[-4]",
            "opacity-[55%]",
        )

    @on(Button.Pressed, "#flip-palette")
    def flip_palette(self) -> None:
        palette = self.query_one("#palette", Static)
        if palette.has_class("bg-[#3f3f46]"):
            palette.remove_class("bg-[#3f3f46]", "text-[#fafafa]")
            palette.add_class("bg-[#f59e0b]", "text-[#1f2937]")
            palette.update("Palette target: bg-[#f59e0b] text-[#1f2937]")
        else:
            palette.remove_class("bg-[#f59e0b]", "text-[#1f2937]")
            palette.add_class("bg-[#3f3f46]", "text-[#fafafa]")
            palette.update("Palette target: bg-[#3f3f46] text-[#fafafa]")


if __name__ == "__main__":
    TailwindArbitraryApp().run()
