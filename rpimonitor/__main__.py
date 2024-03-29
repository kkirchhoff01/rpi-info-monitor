#!/usr/bin/python3

from rpimonitor import display
from rpimonitor.config import SLEEP_TIME
import argparse
import time
import os
try:
    import cursor
except ImportError:
    cursor = None

_clear = lambda: os.system('clear')

def run(vertical=False, colored=True, temp_units=None):
    content = display.get_content(
        temp_units=temp_units,
        vertical=vertical,
        colored=colored,
    )
    if not vertical:
        content = display.rotate(
            content,
            as_string=True,
        )
    else:
        content = '\n'.join(content)
    _clear()
    print(content)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(prog='display')
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
    argparser.add_argument(
        '--no-color',
        '-c',
        action='store_false',
        dest='colored',
    )
    argparser.add_argument(
        '--temp-units',
        '--units',
        '-t',
        type=lambda x: str(x).lower(),
    )
    argparser.add_argument(
        '--refresh',
        type=int,
        default=SLEEP_TIME,
    )
    args = argparser.parse_args()

    if cursor is not None:
        cursor.hide()
    # If run_forever is True, run an
    # infinite loop (e.g. `while True:`)
    while args.run_forever:
        try:
            run(vertical=args.vertical,
                colored=args.colored,
                temp_units=args.temp_units)
            time.sleep(args.refresh)
        except KeyboardInterrupt:
            break
    else:
        content = display.get_content(
            temp_units=args.temp_units,
            vertical=args.vertical,
            colored=args.colored,
        )
        if not args.vertical:
            content = display.rotate(
                content,
                as_string=True,
            )
        else:
            content = '\n'.join(content)
        print(content)
