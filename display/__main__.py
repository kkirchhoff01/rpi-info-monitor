#!/bin/bash

from . import display
from .config import SLEEP_TIME
import subprocess
import argparse
import time


def run():
    content = display.get_content(
        vertical=args.vertical,
    )
    if not args.vertical:
        content = display.rotate(
            content,
            as_string=True,
        )
    else:
        content = '\n'.join(content)
    _ = subprocess.call('clear', shell=True)
    print(content)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--run-forever',
        '--run', '-r',
        action='store_true',
    )
    argparser.add_argument(
        '--vertical',
        '-v',
        action='store_true',
    )
    args = argparser.parse_args()

    # If run_forever is True, run an
    # infinite loop (e.g. `while True:`)
    while args.run_forever:
        try:
            run()
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            break
    else:
        content = display.get_content(
            vertical=args.vertical,
        )
        if not args.vertical:
            content = display.rotate(
                content,
                as_string=True,
            )
        else:
            content = '\n'.join(content)
        print(content)
