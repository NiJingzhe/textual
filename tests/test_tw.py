from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Label

from textual.tw import TailwindTCSS


def test_tailwind_tcss_reuses_normalized_arbitrary_utilities() -> None:
    compiler = TailwindTCSS()

    first_classes = compiler("bg-[#ABCDEF] w-[42]").split()
    second_classes = compiler("bg-[#abcdef] w-[42]").split()

    assert first_classes[0] == second_classes[0]
    assert first_classes[1] == second_classes[1]
    assert compiler.css.count(f".{first_classes[0]}") == 1
    assert compiler.css.count("background:") == 1
    assert "width: 42;" in compiler.css


def test_tailwind_tcss_compiles_hover_variants() -> None:
    compiler = TailwindTCSS()

    alias = compiler("hover:bg-[#334155]")

    assert f".{alias}:hover" in compiler.css
    assert "background: #334155;" in compiler.css


def test_tailwind_tcss_preserves_plain_textual_classes() -> None:
    compiler = TailwindTCSS()

    classes = compiler("existing-class w-[50%]").split()

    assert classes[0] == "existing-class"
    assert classes[1].startswith("_tw_")


def test_tailwind_tcss_is_reexported_from_textual() -> None:
    from textual import TailwindTCSS as ExportedTailwindTCSS
    from textual import tailwind_tcss
    from textual import tw

    assert ExportedTailwindTCSS is TailwindTCSS
    assert callable(tw)
    assert callable(tailwind_tcss)


class ComposeTwApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Label(
            "Hello",
            id="hello",
            classes="w-[42] bg-[#334155] text-[#f8fafc]",
        )


async def test_tailwind_tcss_applies_compiled_styles_during_compose() -> None:
    async with ComposeTwApp().run_test() as pilot:
        label = pilot.app.query_one("#hello", Label)

        assert label.classes == frozenset({"w-[42]", "bg-[#334155]", "text-[#f8fafc]"})
        assert str(label.styles.width) == "42"
        assert label.styles.background == Color.parse("#334155")
        assert label.styles.color == Color.parse("#f8fafc")


class DynamicTwApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Label("Hello", id="hello")


async def test_tailwind_tcss_can_install_rules_after_mount() -> None:
    app = DynamicTwApp()

    async with app.run_test() as pilot:
        label = pilot.app.query_one("#hello", Label)
        label.add_class("opacity-[50%]", "translate-x-[-2]")

        await pilot.pause()

        assert label.has_class("opacity-[50%]", "translate-x-[-2]")
        assert label.styles.opacity == 0.5
        assert str(label.styles.offset.x) == "-2"
        assert str(label.styles.offset.y) == "0"
