---
name: textual
description: Build terminal user interface (TUI) applications with the Textual framework. Use when creating new Textual apps, adding screens/widgets, styling with TCSS or Tailwind utility classes, handling events and reactivity, testing TUI apps, or any task involving "textual", "TUI", or terminal-based Python applications.
---

# Textual TUI Framework

Build terminal applications with Textual's web-inspired architecture: App → Screen → Widget.
Supports both traditional TCSS and **Tailwind-inspired utility classes** for rapid styling.

## Quick Start

### With Tailwind Utility Classes (Recommended)

```python
from textual import tailwind_tcss
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static

class MyApp(App):
    CSS = tailwind_tcss() + """
    Screen { align: center middle; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="border-round px-4 py-2 bg-[#0f172a] w-[42]"):
            yield Static("Hello", classes="text-center text-slate-50")
        yield Footer()

if __name__ == "__main__":
    MyApp().run()
```

### With External TCSS File

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_dark", "Dark Mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, World!")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

if __name__ == "__main__":
    MyApp().run()
```

## App Conventions

### Prefer Tailwind Utility Classes

Always use `tailwind_tcss()` and apply styling via `classes=` on widgets. **Avoid writing CSS with ID selectors** (`#id { ... }`). The only acceptable inline CSS is `Screen { ... }` since Screen cannot receive classes.

```python
# Good: use classes
yield RichLog(id="chat-log", classes="h-fr border p-1")

# Bad: ID selector in CSS
CSS = """
#chat-log { height: 1fr; border: solid; }
"""
```

## Core Concepts

### Widget Lifecycle
1. `__init__()` → `compose()` → `on_mount()` → `on_show()`/`on_hide()` → `on_unmount()`

### Reactivity
```python
from textual.reactive import reactive, var

class MyWidget(Widget):
    count = reactive(0)  # Triggers refresh on change
    internal = var("")   # No automatic refresh

    def watch_count(self, new_value: int) -> None:
        """Called when count changes."""
        self.styles.background = "green" if new_value > 0 else "red"

    def validate_count(self, value: int) -> int:
        """Constrain values."""
        return max(0, min(100, value))
```

### Events and Messages
```python
from textual import on
from textual.message import Message

class MyWidget(Widget):
    class Selected(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def on_click(self) -> None:
        self.post_message(self.Selected("item"))

class MyApp(App):
    # Handler naming: on_<widget>_<message>
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.log(f"Button {event.button.id} pressed")

    @on(Button.Pressed, "#submit")  # CSS selector filtering
    def handle_submit(self) -> None:
        pass
```

### Data Flow
- **Attributes down**: Parent sets child properties directly
- **Messages up**: Child posts messages to parent via `post_message()`

## Screens

```python
from textual.screen import Screen

class WelcomeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Static("Welcome!")
        yield Button("Continue", id="continue")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            self.app.push_screen("main")

class MyApp(App):
    SCREENS = {"welcome": WelcomeScreen, "main": MainScreen}

    def on_mount(self) -> None:
        self.push_screen("welcome")
```

## Custom Widgets

### Simple Widget
```python
class Greeting(Widget):
    def render(self) -> RenderResult:
        return "Hello, [bold]World[/bold]!"
```

### Compound Widget
```python
class LabeledButton(Widget):
    DEFAULT_CSS = """
    LabeledButton { layout: horizontal; height: auto; }
    LabeledButton Label { width: 1fr; }
    """

    def __init__(self, label: str, button_text: str) -> None:
        self.label_text = label
        self.button_text = button_text
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.label_text)
        yield Button(self.button_text)
```

### Focusable Widget
```python
class Counter(Widget):
    can_focus = True
    BINDINGS = [("up", "increment", "+"), ("down", "decrement", "-")]
    count = reactive(0)

    def action_increment(self) -> None:
        self.count += 1
```

## Layout Patterns

### Containers
```python
from textual.containers import Horizontal, Vertical, Grid, VerticalScroll

def compose(self) -> ComposeResult:
    with Vertical():
        with Horizontal():
            yield Button("Left")
            yield Button("Right")
        with VerticalScroll():
            for i in range(100):
                yield Label(f"Item {i}")
```

### Grid CSS
```css
Grid {
    layout: grid;
    grid-size: 3 2;           /* columns rows */
    grid-columns: 1fr 2fr 1fr;
    grid-gutter: 1 2;
}
#wide { column-span: 2; }
```

### Docking
```css
#header { dock: top; height: 3; }
#sidebar { dock: left; width: 25; }
#footer { dock: bottom; height: 1; }
```

## Tailwind TCSS Utility Classes

Textual ships with a bundled `tailwind.tcss` utility sheet for utility-class styling (like Tailwind CSS).

### Loading the Utility Sheet

```python
from textual import tailwind_tcss
from textual.app import App

class MyApp(App):
    # Inline with custom CSS
    CSS = tailwind_tcss() + """
    Screen { align: center middle; }
    """

    # Or load as a file via CSS_PATH
    # CSS_PATH = "tailwind.tcss"  # exported with: export-twcss ./
```

### Using Utility Classes

Apply classes via the `classes` parameter on any widget:

```python
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label

def compose(self):
    with Vertical(classes="gap-2 p-4 bg-slate-900"):
        yield Label("Title", classes="text-center font-bold text-slate-50")
        with Horizontal(classes="gap-4"):
            yield Button("OK", classes="bg-blue-500 text-white")
            yield Button("Cancel", classes="bg-slate-700 text-slate-300")
```

### Arbitrary Values

Use bracket syntax for custom values: `property-[value]`

```python
classes="w-[42] bg-[#334155] text-[#f8fafc] opacity-[55%]"
```

### Pseudo-class Prefixes

Combine with Textual pseudo-classes: `prefix:class`

```python
classes="hover:bg-blue-700 focus:border-round dark:hover:bg-slate-700"
classes="focus-within:bg-[#1e293b] odd:bg-[#0f172a]"
classes="disabled:opacity-[50%]"
```

Supported prefixes: `hover`, `focus`, `blur`, `focus-within`, `disabled`, `enabled`, `dark`, `light`, `first-child`, `last-child`, `odd`, `even`, `empty`.

### Transition Utilities

Combine transition utilities with state changes for animations:

```python
classes="transition-colors hover:bg-blue-700"
classes="transition-all focus:border-round"
classes="transition-opacity hover:opacity-[50%]"
classes="transition-basic"
classes="transition-slow-colors"
```

Available transitions: `transition-colors`, `transition-opacity`, `transition-offset`, `transition-size`, `transition-basic`, `transition-slow-colors`, `transition-all`.

### Available Utility Classes (Bundled)

**Layout**: `block`, `hidden`, `visible`, `invisible`, `relative`, `absolute`, `layout-horizontal`, `layout-vertical`, `layout-stream`, `grid`

**Docking**: `dock-top`, `dock-right`, `dock-bottom`, `dock-left`

**Overflow**: `overflow-auto`, `overflow-hidden`, `overflow-scroll`, `overflow-x-auto`, `overflow-y-hidden`, etc.

**Alignment**: `align-center`, `align-top-left`, `align-middle-right`, `align-x-center`, `align-y-middle`, `content-center`, `content-x-left`, `content-y-bottom`, etc.

**Spacing**: `p-0/1/2/4`, `px-0/1/2/4`, `py-0/1/2/4`, `pl-0/1/2/4`, `pr-0/1/2/4`, `pt-0/1/2/4`, `pb-0/1/2/4`, `m-0/1/2/4`, `mx-0/1/2/4`, `my-0/1/2/4`, `ml-0/1/2/4`, `mr-0/1/2/4`, `mt-0/1/2/4`, `mb-0/1/2/4`

**Sizing**: `w-auto`, `w-full`, `w-screen`, `w-fr`, `h-auto`, `h-full`, `h-screen`, `h-fr`, `min-w-0`, `min-h-0`, `max-w-full`, `max-h-full`

**Text**: `text-left/center/right/justify/start/end`, `text-wrap/nowrap/clip/fold/ellipsis`, `font-normal/bold/italic`, `underline`, `line-through`, `reverse`

**Colors**: `bg-transparent/white/black`, `bg-slate-50/300/500/700/900`, `bg-blue-500/700`, `bg-emerald-500/700`, `bg-amber-500`, `bg-red-500`, `text-white/black`, `text-slate-50/300/500/700/900`, `text-blue-500/700`, `text-emerald-500/700`, `text-amber-500`, `text-red-500`

**Borders**: `border`, `border-none`, `border-dashed`, `border-double`, `border-heavy`, `border-round`, `border-t/r/b/l`, `border-x`, `border-y`, `border-slate-300`, `border-blue-500`, `border-emerald-500`, `border-amber-500`, `border-red-500`, `outline`, `outline-none`, `outline-dashed`, `outline-double`

**Grid**: `grid-cols-1/2/3/4`, `grid-rows-1/2/3/4`, `col-span-1/2/3/4`, `row-span-1/2/3/4`, `gap-0/1/2/4`, `gap-x-1/2/4`, `gap-y-1/2/4`

**Cursor**: `cursor-default/pointer/text/wait/grab/grabbing/move`

**Tint**: `tint-white-10`, `tint-black-10`

**Expand**: `expand-greedy`, `expand-optimal`

### Palette Variables (TCSS)

```css
$tw-slate-50: #f8fafc;    $tw-slate-300: #cbd5e1;    $tw-slate-500: #64748b;
$tw-slate-700: #334155;    $tw-slate-900: #0f172a;
$tw-blue-500: #3b82f6;     $tw-blue-700: #1d4ed8;
$tw-emerald-500: #10b981;  $tw-emerald-700: #047857;
$tw-amber-500: #f59e0b;    $tw-red-500: #ef4444;
$tw-transition-fast: 120ms out_cubic 0ms;
$tw-transition-normal: 180ms out_cubic 0ms;
$tw-transition-slow: 280ms in_out_cubic 0ms;
```

### Exporting the Sheet as a File

```bash
export-twcss ./styles                    # writes tailwind.tcss to ./styles/
export-twcss ./styles/tw.tcss            # writes to specific file
export-twcss --stdout > ./styles/tw.tcss # writes to stdout
```

Then reference it: `CSS_PATH = "styles/tailwind.tcss"`

## Workers (Async)

```python
from textual import work

class MyApp(App):
    @work(exclusive=True)  # Cancels previous
    async def fetch_data(self, url: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            self.query_one("#result").update(response.text)

    @work(thread=True)  # For sync APIs
    def sync_operation(self) -> None:
        result = blocking_call()
        self.call_from_thread(self.update_ui, result)
```

## Testing

```python
async def test_app():
    app = MyApp()
    async with app.run_test() as pilot:
        await pilot.press("enter")
        await pilot.click("#button")
        await pilot.pause()  # Wait for messages
        assert app.query_one("#status").render() == "Done"
```

## Common Operations

```python
# Query widgets
self.query_one("#id")
self.query_one(Button)
self.query(".class")

# CSS classes
widget.add_class("active")
widget.toggle_class("visible")
widget.set_class(condition, "active")

# Visibility
widget.display = True/False

# Mount/remove
self.mount(NewWidget())
widget.remove()

# Timers
self.set_interval(1.0, callback)
self.set_timer(5.0, callback)

# Exit
self.exit(return_code=0)
```

## References

- **Widget catalog and messages**: See [references/widgets.md](references/widgets.md)
- **CSS properties, selectors, and Tailwind utilities**: See [references/css.md](references/css.md)
- **Complete examples**: See [references/examples.md](references/examples.md)
- **Tailwind utility source**: `src/textual/tailwind.tcss`
- **Official docs**: https://textual.textualize.io/
