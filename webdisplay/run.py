#!/usr/bin/python3

from rpimonitor import display
from rpimonitor.constants import Styles, TempUnits
from rpimonitor.config import HOSTS, VALID_STYLES
from webdisplay.config import (
    TEMPLATE_PATH,
    PORT,
    DEFAULT_FONT,
    VERT_FONT,
    MOBILE_HOR_FONT,
    MOBILE_VERT_FONT,
    MOBILE_WEIGHT_FONT,
    BASE_DISPLAY,
    FONT_UNIT,
    MIN_FONT,
)
from flask import (
    Flask,
    Response,
    request,
    render_template,
)
try:
    from markupsafe import Markup
except ImportError:
    Markup = None
try:
    from flask_mobility import Mobility
except ImportError:
    Mobility = None

COLOR_MAP = {
    Styles.RED: '<span class="red">',
    Styles.GREEN: '<span class="green">',
    Styles.OKBLUE: '<span class="blue">',
    Styles.BOLD: '<span class="converted-bold">',
    Styles.ENDC: '</span>',
}

app = Flask(
    __name__,
    template_folder=TEMPLATE_PATH,
)

if Mobility is not None:
    Mobility(app)


def get_font(default=DEFAULT_FONT):
    """Adjust size of font for number of panels"""
    # Don't adjust if there are less than 3 panels
    adjust_weight = max(0, len(HOSTS) - BASE_DISPLAY)

    # Reduce the original font size by a weight
    # proportional to the number of displays
    return max(
        default - adjust_weight * FONT_UNIT,
        MIN_FONT,
    )

def _convert_colors(content):
    new_content = []
    is_list = isinstance(content, (list, tuple))
    if not is_list:
        content = [content]
    
    for row in content:
        if isinstance(row, (list, tuple)):
            new_content.append(_convert_colors(row))
            continue
        for color in VALID_STYLES:
            new_color = COLOR_MAP.get(color, '<span>')
            row = row.replace(color, new_color)
    
        new_content.append(row)

    if not is_list:
        return new_content[0]
    
    return new_content

@app.route('/')
def index():
    try:
        is_mobile = (
            Mobility is not None and
            request.MOBILE
        )

        orient = request.args\
            .get('orientation')
        if orient is not None:
            vertical = (orient.lower() == 'vertical')
        else:
            vertical = is_mobile

        mode = request.args\
            .get('mode', 'light')
        mode = (
            'dark-mode' if mode.lower() == 'dark'
            else 'light-mode'
        )

        temp_units = request.args\
            .get('temp_units', TempUnits.CELSIUS)

        refresh_rate = request.args\
            .get('refresh', 30)
        if not isinstance(refresh_rate, int):
            if not refresh_rate.isnumeric():
                raise ValueError(
                    'Invalid refresh rate: '
                    f'{refresh_rate}. Must be '
                    'an integer'
                )
            refresh_rate = int(refresh_rate)

        if Markup is not None:
            colored = request.args\
                .get('color', True)
            if isinstance(colored, str):
                colored = (
                    True if colored.lower() 
                        in ('true', '1')
                    else False
                )
        else:
            colored = False

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

        if colored and Markup is not None:
            content = Markup(_convert_colors(content))
        
        if not vertical:
            fontsize = (
                MOBILE_HOR_FONT if is_mobile 
                else DEFAULT_FONT
            )
            fontsize = get_font(fontsize)
        else:
            if colored:
                fontsize = (
                    MOBILE_WEIGHT_FONT if is_mobile 
                    else VERT_FONT
                )
            else:
                fontsize = (
                    MOBILE_VERT_FONT if is_mobile 
                    else VERT_FONT
                )

        return render_template(
            'index.html',
            content=content,
            fontsize=fontsize,
            refresh=refresh_rate,
            mode=mode,
            is_mobile_vert=(
                "true" if vertical
                else ""
            ),
        )
    except Exception as e:
        return Response(
            f'Error: {e}',
            status=500,
        )


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
