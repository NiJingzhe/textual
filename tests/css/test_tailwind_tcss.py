import pytest

from textual import tailwind_tcss
from textual.cli import export_twcss
from textual.css.stylesheet import Stylesheet


def test_tailwind_stylesheet_parses() -> None:
    """The Tailwind-style utility stylesheet should remain parseable."""

    stylesheet = Stylesheet()
    stylesheet.add_source(tailwind_tcss(), read_from=("test", "tailwind.tcss"))
    stylesheet.parse()

    assert ".border-round" in stylesheet.css
    assert ".px-4" in stylesheet.css
    assert ".transition-basic" in stylesheet.css
    assert ".transition-all" in stylesheet.css
    assert ".hover-bg-blue-700:hover" not in stylesheet.css
    assert ".w-40" not in stylesheet.css


def test_export_twcss_to_directory(tmp_path, capsys) -> None:
    result = export_twcss([str(tmp_path)])
    output_path = tmp_path / "tailwind.tcss"

    assert result == 0
    assert output_path == tmp_path / "tailwind.tcss"
    assert output_path.read_text(encoding="utf-8") == tailwind_tcss()
    assert capsys.readouterr().out.strip() == str(output_path)


def test_export_twcss_to_explicit_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "utilities" / "textual-tailwind.tcss"
    result = export_twcss([str(output_path)])

    assert result == 0
    assert output_path == tmp_path / "utilities" / "textual-tailwind.tcss"
    assert output_path.read_text(encoding="utf-8") == tailwind_tcss()
    assert capsys.readouterr().out.strip() == str(output_path)


def test_export_twcss_refuses_to_overwrite_without_force(tmp_path, capsys) -> None:
    output_path = tmp_path / "tailwind.tcss"
    assert export_twcss([str(tmp_path)]) == 0

    result = export_twcss([str(output_path)])

    assert result == 1
    assert (
        "Refusing to overwrite existing Tailwind TCSS file" in capsys.readouterr().err
    )


def test_export_twcss_overwrites_with_force(tmp_path) -> None:
    output_path = tmp_path / "tailwind.tcss"
    output_path.write_text("stale", encoding="utf-8")

    result = export_twcss([str(output_path), "--force"])

    assert result == 0
    assert output_path.read_text(encoding="utf-8") == tailwind_tcss()


def test_export_twcss_stdout(capsys) -> None:
    result = export_twcss(["--stdout"])

    assert result == 0
    captured = capsys.readouterr()
    assert captured.out == tailwind_tcss()
    assert captured.err == ""


def test_export_twcss_rejects_destination_with_stdout() -> None:
    with pytest.raises(SystemExit):
        export_twcss(["--stdout", "./styles"])
