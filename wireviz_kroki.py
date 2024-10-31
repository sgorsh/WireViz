#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, io
import argparse
import traceback
import wireviz.wireviz as wv
from wireviz import __version__

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
"""Wireviz Kroki wrapper.
Reads YAML data from stdin and writes output to stdout.
Errors and messages from WireViz are printed to stderr.""")   
 
    output_formats = ["svg", "png", "harness"]

    parser.add_argument("--format", "-f", type=str, required=True, choices=output_formats, 
                        help=f"Supported output formats.")
    parser.add_argument("input", type=str, choices=["-"], help="'-' for stdin")
    parser.add_argument("-o", type=str, choices=["-"], help="'-' for stdout")
    parser.add_argument("--version", "-v", action="version", version=__version__, help="print WireViz version")

    args = parser.parse_args()

    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        data = wv.parse(inp = sys.stdin.read(), return_types=args.format)

        # Restore stdout
        sys.stdout = old_stdout

        if isinstance(data, str):
            sys.stdout.write(data)
        elif isinstance(data, bytes):
            sys.stdout.buffer.write(data)
        else:
            raise ValueError("Unsupported data format")
        sys.exit(0)

    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n-----------\n")
        sys.stderr.write(traceback.format_exc())
        sys.exit(1)
