from __future__ import annotations

import argparse
import sys
from typing import Sequence

from textual.tw import _write_tailwind_tcss, tailwind_tcss


def export_twcss(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for exporting the bundled Tailwind-style TCSS."""

    parser = argparse.ArgumentParser(
        prog="export-twcss",
        description="Write Textual's bundled Tailwind-style TCSS to a file.",
    )
    parser.add_argument(
        "destination",
        nargs="?",
        help=(
            "Destination directory or file path. Directories receive a "
            "'tailwind.tcss' file."
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite the destination if it already exists.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write the bundled TCSS to stdout instead of a file.",
    )
    args = parser.parse_args(argv)

    if args.stdout:
        if args.destination is not None:
            parser.error("destination may not be provided with --stdout")
        print(tailwind_tcss(), end="")
        return 0

    if args.destination is None:
        parser.error("destination is required unless --stdout is used")

    try:
        output_path = _write_tailwind_tcss(args.destination, overwrite=args.force)
    except FileExistsError as error:
        print(str(error), file=sys.stderr)
        return 1

    print(output_path)
    return 0
