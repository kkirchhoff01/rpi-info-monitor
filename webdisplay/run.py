#!/usr/bin/python3

import sys
import os
displaypath = os.path.join(
    os.path.dirname(__file__),
    '..',
)
sys.path.insert(0, os.path.abspath(displaypath))
import display
import functools
import datetime
import requests
import psutil
from flask import (
    Flask,
    Response,
    request,
    render_template,
)
try:
    from flask_mobility import Mobility
except ImportError:
    Mobility = None
import socket
import json
import copy
import time

app = Flask('rpiwebdisplay')

# Optional dependency
if Mobility is not None:
    Mobility(app)

PORT = 5100


def get_formatted_content():
    content = display.get_content(
        vertical=args.vertical,
    )
    if not vertical:
        content = display.rotate(
            content,
            as_string=True,
        )
    else:
        content = '\n'.join(content)

@app.route('/')
def index():
    try:
        orient = request.args\
            .get('orientation', 'vertical')
        vertical = (orient.lower() == 'vertical')

        content = display.get_content(
            vertical=vertical,
        )
        if not vertical:
            content = display.rotate(
                content,
                as_string=True,
            )
        else:
            content = '\n'.join(content)

        if request.MOBILE:
            fontsize = 27
        else:
            fontsize = (18 if not vertical else 14)

        return render_template(
            'index.html',
            content=content,
            fontsize=fontsize,
        )
    except Exception as e:
        return render_template(
            'index.html',
            content=f'Error: {e}',
            fontsize=14,
        )


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
