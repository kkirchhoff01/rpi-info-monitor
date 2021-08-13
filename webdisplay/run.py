#!/usr/bin/python3

import sys
import os
displaypath = os.path.join(
    os.path.dirname(__file__),
    '..',
)
sys.path.insert(0, os.path.abspath(displaypath))
import display
from flask import (
    Flask,
    request,
    render_template,
)
try:
    from flask_mobility import Mobility
except ImportError:
    Mobility = None

app = Flask('rpiwebdisplay')

# Optional dependency
if Mobility is not None:
    Mobility(app)

PORT = 5100
DEFAULT_FONT = 18
MOBILE_FONT = 27
VERT_FONT = 14


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

        if Mobility is not None and \
                request.MOBILE:
            fontsize = MOBILE_FONT
        else:
            fontsize = (
                DEFAULT_FONT if not vertical
                else VERT_FONT
            )

        return render_template(
            'index.html',
            content=content,
            fontsize=fontsize,
        )
    except Exception as e:
        return render_template(
            'index.html',
            content=f'Error: {e}',
            fontsize=DEFAULT_FONT,
        )


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
