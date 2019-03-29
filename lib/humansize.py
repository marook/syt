import math
import re

units = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']

bytes_template = '%1.0f'
default_template = '%1.1f'

def format_size(size, suffix='B'):
    for i, unit in enumerate(units):
        if size < 1024.0:
            template = bytes_template if i == 0 else default_template
            return  (template + '%s%s') % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Y', suffix)

size_pattern = re.compile('^([0-9]+)\s*([{}]?)B?$'.format(''.join(units)))

def parse_size(size_str):
    m = size_pattern.match(size_str)
    if not m:
        raise IllegalSizeString('size string can\'t be parsed: {}'.format(size_str))
    size = int(m.group(1))
    unit = m.group(2)
    unit_modifier = math.pow(1024, units.index(unit))
    return size * unit_modifier

class IllegalSizeString(Exception):
    pass

