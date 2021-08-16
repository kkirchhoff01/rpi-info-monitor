

class Styles:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    GREEN = OKGREEN = '\033[92m'
    YELLOW = WARNING = '\033[93m'
    RED = FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TempUnits:
    C = CELSIUS = 'celsius'
    F = FAHRENHEIT = 'fahrenheit'


__all__ = [
    'Styles',
    'TempUnits',
]
