#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Entry point for the project.

import argparse
import src.examples as ex
from src.utils import load_config


def _menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="👾 Fixed Computational Graph Example 👾"
    )
    parser.add_argument(
        "-e",
        dest="examples",
        action="store_true",
        help="Run examples for quadratic and cubic polynomial functions.",
    )
    parser.add_argument(
        "-a",
        dest="api",
        action="store_true",
        help="Run an example that utilizes a hint for a constrained none.",
    )
    return parser


def run() -> None:

    parser = _menu()
    args = parser.parse_args()

    if args.examples:
        ex.quadratic()
        ex.cubic()

    elif args.api:
        ex.hint_for_division()

    else:
        parser.print_help()


if __name__ == "__main__":
    load_config()
    run()
