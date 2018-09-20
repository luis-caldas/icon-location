# -*- coding: utf-8 -*-

import sys


def show(error_string, argparse_object, bad=False):

    colors = {
        "yellow": "\033[33m",
        "red": "\033[31m",
        "bold": "\033[1m",
        "end": "\033[0m"
    }

    warning_sign = "%s%s[%s!%s%s]%s" % (
        colors["end"], colors["bold"],
        colors["red" if bad else "yellow"], colors["end"], colors["bold"],
        colors["end"]
    )

    # print the argparse help
    argparse_object.print_help()

    # simple error handler
    print("\n%s %s\n" % (
        warning_sign,
        error_string
    ))

    sys.exit(1)
