from __future__ import annotations

import hashlib
import re
import weakref
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from itertools import count
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from textual._context import active_app
from textual.css.constants import VALID_PSEUDO_CLASSES
from textual.css.styles import Styles
from textual.css.tokenize import IDENTIFIER

if TYPE_CHECKING:
    from os import PathLike

    from textual.app import App


__all__ = [
    "TailwindTCSS",
    "install_tw",
    "tailwind_tcss",
    "tw",
    "tw_css",
]


_ARBITRARY_UTILITY_RE = re.compile(r"^(?P<utility>[a-z][a-z0-9-]*)-\[(?P<value>.+)\]$")
_INVALID_VALUE_CHARS_RE = re.compile(r"[;{}\n\r]")
_SANITIZE_RE = re.compile(r"[^a-z0-9_-]+")
_COMPRESS_RE = re.compile(r"_+")
_IDENTIFIER_RE = re.compile(IDENTIFIER)
_CLASS_START_RE = re.compile(r"^\.(?P<name>[a-zA-Z0-9_-]+)\s*\{$")
_VARIABLE_RE = re.compile(r"^\$(?P<name>[a-zA-Z0-9_-]+):\s*(?P<value>.+);$")
_VARIABLE_REFERENCE_RE = re.compile(r"\$([a-zA-Z0-9_-]+)")

_UTILITY_TO_DECLARATION = {
    "bg": "background",
    "h": "height",
    "max-h": "max-height",
    "max-w": "max-width",
    "min-h": "min-height",
    "min-w": "min-width",
    "opacity": "opacity",
    "text": "color",
    "text-opacity": "text-opacity",
    "tint": "tint",
    "translate-x": "offset-x",
    "translate-y": "offset-y",
    "w": "width",
}


@dataclass(frozen=True)
class CompiledUtility:
    """A compiled Tailwind-style utility class and its generated TCSS."""

    alias: str
    css_rule: str
    signature: str


@lru_cache(maxsize=1)
def _static_utility_declarations() -> dict[str, tuple[str, ...]]:
    """Return normalized declaration lines for bundled static utilities."""

    variables: dict[str, str] = {}
    declarations_by_class: dict[str, tuple[str, ...]] = {}
    current_class: str | None = None
    current_lines: list[str] = []
    in_comment = False

    def strip_comments(line: str) -> str:
        nonlocal in_comment
        while line:
            if in_comment:
                _, end, after = line.partition("*/")
                if not end:
                    return ""
                line = after
                in_comment = False
                continue
            before, start, after = line.partition("/*")
            if not start:
                return before
            in_comment = True
            line = before + after
        return line

    def resolve_variable(name: str, seen: set[str] | None = None) -> str:
        if seen is None:
            seen = set()
        if name in seen:
            raise ValueError(f"Circular Tailwind TCSS variable reference ${name}")
        seen.add(name)
        try:
            value = variables[name]
        except KeyError as error:
            raise ValueError(f"Unknown Tailwind TCSS variable ${name}") from error
        return _VARIABLE_REFERENCE_RE.sub(
            lambda match: resolve_variable(match.group(1), seen.copy()), value
        )

    def normalize_block(class_name: str, lines: list[str]) -> tuple[str, ...]:
        resolved_lines = [
            _VARIABLE_REFERENCE_RE.sub(
                lambda match: resolve_variable(match.group(1)), line
            )
            for line in lines
        ]
        try:
            styles = Styles.parse(
                "\n".join(resolved_lines),
                read_from=("textual.tw", f"tailwind.tcss:{class_name}"),
            )
        except Exception as error:
            raise ValueError(
                f"Unable to parse bundled utility {class_name!r}; {error}"
            ) from None
        normalized_lines = tuple(styles.css_lines)
        if not normalized_lines:
            normalized_lines = tuple(line for line in resolved_lines if line)
        if not normalized_lines:
            raise ValueError(f"Bundled utility {class_name!r} produced no declarations")
        return normalized_lines

    for raw_line in tailwind_tcss().splitlines():
        line = strip_comments(raw_line).strip()
        if not line:
            continue

        if current_class is None:
            variable_match = _VARIABLE_RE.match(line)
            if variable_match is not None:
                variables[variable_match.group("name")] = variable_match.group("value")
                continue

            class_match = _CLASS_START_RE.match(line)
            if class_match is not None:
                current_class = class_match.group("name")
                current_lines = []
                continue
            continue

        if line == "}":
            declarations_by_class[current_class] = normalize_block(
                current_class, current_lines
            )
            current_class = None
            current_lines = []
            continue

        current_lines.append(line)

    if current_class is not None:
        raise ValueError(f"Unterminated bundled utility class {current_class!r}")

    return declarations_by_class


@lru_cache(maxsize=1)
def tailwind_tcss() -> str:
    """Return the bundled Tailwind-style TCSS core utility sheet."""

    return files("textual").joinpath("tailwind.tcss").read_text(encoding="utf-8")


def _write_tailwind_tcss(
    destination: str | PathLike[str], *, overwrite: bool = False
) -> Path:
    """Write the bundled Tailwind-style TCSS to a directory or file path.

    If ``destination`` is a directory, the stylesheet is written as
    ``tailwind.tcss`` inside that directory.
    """

    destination_path = Path(destination)
    output_path = (
        destination_path / "tailwind.tcss"
        if destination_path.is_dir() or not destination_path.suffix
        else destination_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Refusing to overwrite existing Tailwind TCSS file at {output_path}"
        )
    output_path.write_text(tailwind_tcss(), encoding="utf-8")
    return output_path


class TailwindTCSS:
    """Compile Tailwind-like utility tokens into valid Textual classes and TCSS.

    Example:
        ```python
        from textual import tw

        yield Label("Hello", classes=tw("w-[42] bg-[#334155] text-[#f8fafc]"))
        ```
    """

    _instance_counter = count(1)

    def __init__(self, source_name: str | None = None) -> None:
        if source_name is None:
            index = next(self._instance_counter)
            source_name = "textual.tw" if index == 1 else f"textual.tw.{index}"
        self._read_from = (__file__, source_name)
        self._compiled_by_token: dict[str, CompiledUtility] = {}
        self._compiled_by_signature: dict[str, CompiledUtility] = {}
        self._synced_versions: weakref.WeakKeyDictionary[App[object], int] = (
            weakref.WeakKeyDictionary()
        )
        self._version = 0

    def __call__(self, utilities: str, *, app: App[object] | None = None) -> str:
        return self.classes(utilities, app=app)

    @property
    def css(self) -> str:
        """Compiled TCSS for all arbitrary utilities seen by this registry."""

        return "\n\n".join(
            compiled.css_rule
            for compiled in sorted(
                self._compiled_by_signature.values(),
                key=lambda compiled: compiled.alias,
            )
        )

    def classes(self, utilities: str, *, app: App[object] | None = None) -> str:
        """Compile utility tokens and return valid Textual class names."""

        compiled_class_names: list[str] = []
        has_new_rules = False

        for token in utilities.split():
            if self._requires_compilation(token):
                compiled, was_new = self._compile_token(token)
                compiled_class_names.append(compiled.alias)
                has_new_rules = has_new_rules or was_new
            else:
                self._validate_identifier(token)
                compiled_class_names.append(token)

        if not compiled_class_names:
            return ""

        app = app if app is not None else self._get_active_app()
        self._maybe_install(app, has_new_rules, refresh=bool(app and app._is_mounted))

        return " ".join(compiled_class_names)

    def preprocess(
        self,
        class_names: Iterable[str],
        *,
        app: App[object] | None = None,
        refresh: bool = False,
    ) -> tuple[set[str], set[str]]:
        """Normalize raw class names and compile arbitrary utilities.

        Returns a tuple of raw class names and generated alias class names.
        """

        raw_classes: set[str] = set()
        compiled_classes: set[str] = set()
        has_new_rules = False

        for token in class_names:
            if self._requires_compilation(token):
                compiled, was_new = self._compile_token(token)
                raw_classes.add(token)
                compiled_classes.add(compiled.alias)
                has_new_rules = has_new_rules or was_new
            else:
                self._validate_identifier(token)
                raw_classes.add(token)

        self._maybe_install(app, has_new_rules, refresh=refresh)
        return raw_classes, compiled_classes

    def install(self, app: App[object], *, refresh: bool = True) -> None:
        """Install compiled TCSS into an app's stylesheet."""

        if not self._compiled_by_signature or not hasattr(app, "stylesheet"):
            return

        app.stylesheet.add_source(
            self.css,
            read_from=self._read_from,
            is_default_css=False,
        )
        self._synced_versions[app] = self._version
        if refresh and app._is_mounted:
            app.refresh_css()

    @staticmethod
    def _get_active_app() -> App[object] | None:
        try:
            return active_app.get()
        except LookupError:
            return None

    @staticmethod
    def _requires_compilation(token: str) -> bool:
        return "[" in token or "]" in token or ":" in token

    @staticmethod
    def _validate_identifier(token: str) -> None:
        if _IDENTIFIER_RE.fullmatch(token) is None:
            from textual.dom import BadIdentifier

            raise BadIdentifier(
                f"{token!r} is an invalid class name; identifiers must contain only "
                "letters, numbers, underscores, or hyphens, and must not begin with a number."
            )

    def _maybe_install(
        self,
        app: App[object] | None,
        has_new_rules: bool,
        *,
        refresh: bool,
    ) -> None:
        if (
            app is None
            or not hasattr(app, "stylesheet")
            or not self._compiled_by_signature
        ):
            return
        synced_version = self._synced_versions.get(app)
        if has_new_rules or synced_version != self._version:
            self.install(app, refresh=refresh)

    def _compile_token(self, token: str) -> tuple[CompiledUtility, bool]:
        try:
            return self._compiled_by_token[token], False
        except KeyError:
            pass

        pseudo_classes, base_utility = self._split_variants(token)
        normalized_lines = self._resolve_utility_declarations(
            token, pseudo_classes, base_utility
        )
        signature = self._make_signature(pseudo_classes, normalized_lines)

        compiled = self._compiled_by_signature.get(signature)
        is_new = compiled is None
        if compiled is None:
            alias = self._make_alias(signature, normalized_lines)
            compiled = CompiledUtility(
                alias=alias,
                css_rule=self._make_css_rule(alias, pseudo_classes, normalized_lines),
                signature=signature,
            )
            self._compiled_by_signature[signature] = compiled
            self._version += 1

        self._compiled_by_token[token] = compiled
        return compiled, is_new

    def _resolve_utility_declarations(
        self,
        token: str,
        pseudo_classes: tuple[str, ...],
        base_utility: str,
    ) -> tuple[str, ...]:
        arbitrary_utility = self._parse_arbitrary_utility(token, base_utility)
        if arbitrary_utility is not None:
            utility_name, raw_value = arbitrary_utility
            declaration_name = _UTILITY_TO_DECLARATION.get(utility_name)
            if declaration_name is None:
                supported = ", ".join(sorted(_UTILITY_TO_DECLARATION))
                raise ValueError(
                    f"Unsupported arbitrary utility {utility_name!r} in {token!r}; "
                    f"supported utilities: {supported}"
                )
            return self._normalize_declarations(token, declaration_name, raw_value)

        if pseudo_classes:
            try:
                return _static_utility_declarations()[base_utility]
            except KeyError:
                raise ValueError(
                    f"Unsupported utility token {token!r}; pseudo variants currently support "
                    "arbitrary utilities and bundled static tailwind.tcss utilities."
                ) from None

        raise ValueError(
            f"Unsupported utility token {token!r}; use a bundled static utility or arbitrary-value syntax like 'w-[42]'"
        )

    @staticmethod
    def _split_variants(token: str) -> tuple[tuple[str, ...], str]:
        parts: list[str] = []
        current: list[str] = []
        bracket_depth = 0

        for character in token:
            if character == "[":
                bracket_depth += 1
            elif character == "]":
                bracket_depth -= 1
                if bracket_depth < 0:
                    raise ValueError(f"Invalid utility token {token!r}")
            if character == ":" and bracket_depth == 0:
                parts.append("".join(current))
                current.clear()
            else:
                current.append(character)

        if bracket_depth != 0:
            raise ValueError(f"Invalid utility token {token!r}")

        parts.append("".join(current))
        if any(not part for part in parts):
            raise ValueError(f"Invalid utility token {token!r}")

        pseudo_classes = tuple(parts[:-1])
        invalid_pseudo_classes = [
            pseudo_class
            for pseudo_class in pseudo_classes
            if pseudo_class not in VALID_PSEUDO_CLASSES
        ]
        if invalid_pseudo_classes:
            invalid = ", ".join(repr(name) for name in invalid_pseudo_classes)
            raise ValueError(f"Unsupported pseudo class in {token!r}: {invalid}")

        return pseudo_classes, parts[-1]

    @staticmethod
    def _parse_arbitrary_utility(
        token: str, base_utility: str
    ) -> tuple[str, str] | None:
        match = _ARBITRARY_UTILITY_RE.fullmatch(base_utility)
        if match is None:
            return None
        utility_name = match.group("utility")
        raw_value = match.group("value")
        if _INVALID_VALUE_CHARS_RE.search(raw_value):
            raise ValueError(f"Invalid arbitrary value in {token!r}")
        return utility_name, raw_value

    @staticmethod
    def _normalize_declarations(
        token: str, declaration_name: str, raw_value: str
    ) -> tuple[str, ...]:
        try:
            styles = Styles.parse(
                f"{declaration_name}: {raw_value};",
                read_from=("textual.tw", token),
            )
        except Exception as error:
            raise ValueError(f"Invalid utility token {token!r}; {error}") from None

        normalized_lines = tuple(styles.css_lines)
        if not normalized_lines:
            raise ValueError(f"Utility token {token!r} produced no declarations")
        return normalized_lines

    @staticmethod
    def _make_signature(
        pseudo_classes: tuple[str, ...], normalized_lines: tuple[str, ...]
    ) -> str:
        pseudo_signature = ":".join(pseudo_classes)
        declaration_signature = "|".join(normalized_lines)
        return f"{pseudo_signature}|{declaration_signature}"

    @staticmethod
    def _make_alias(signature: str, normalized_lines: tuple[str, ...]) -> str:
        readable = "_".join(line.rstrip(";") for line in normalized_lines).lower()
        readable = _SANITIZE_RE.sub("_", readable)
        readable = _COMPRESS_RE.sub("_", readable).strip("_") or "utility"
        readable = readable[:48].rstrip("_")
        digest = hashlib.blake2b(signature.encode("utf-8"), digest_size=4).hexdigest()
        return f"_tw_{readable}_{digest}"

    @staticmethod
    def _make_css_rule(
        alias: str,
        pseudo_classes: tuple[str, ...],
        normalized_lines: tuple[str, ...],
    ) -> str:
        pseudo_suffix = "".join(f":{pseudo_class}" for pseudo_class in pseudo_classes)
        declarations = "\n".join(f"    {line}" for line in normalized_lines)
        return f".{alias}{pseudo_suffix} {{\n{declarations}\n}}"


tw = TailwindTCSS("textual.tw")


def install_tw(app: App[object], *, refresh: bool = True) -> None:
    """Install all compiled utilities from the global registry into an app."""

    tw.install(app, refresh=refresh)


def tw_css() -> str:
    """Return the global registry's compiled TCSS."""

    return tw.css
