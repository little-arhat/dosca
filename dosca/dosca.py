# -*- coding: utf-8 -*-

try:
    from __builtin__ import reduce
except ImportError:
    from functools import reduce

class ParseError(ValueError):
    pass


def parse_file(filename, custom_parsers=None):
    with open(filename) as fileobj:
        return parse(fileobj, custom_parsers=custom_parsers)


def parse(fileobj, custom_parsers=None):
    section_stack = []
    res = {}
    for line in fileobj:
        line = line.strip()
        if not line:
            continue
        elif line.startswith('['):
            (depth, section_name) = parse_section(line)
            diff = len(section_stack) - depth + 1
            if diff < 0:
                msg = 'Too high depth for subsection, missed previous'
                raise ParseError(msg)
            for _ in range(diff):
                section_stack.pop()

            reduce(dict.__getitem__, section_stack, res)[section_name] = {}
            section_stack.append(section_name)
        elif line.startswith('#'):
            pass
        elif '=' in line:
            (key, value) = parse_assignment(line, custom_parsers=custom_parsers)
            reduce(dict.__getitem__, section_stack, res)[key] = value
        else:
            raise ParseError('Unrecognized line: `{0}`'.format(line))
    return res


def parse_section(line):
    depth = line.count('[')
    if depth != line.count(']'):
        msg = 'Unbalanced brackets in section definition: `{0}`'.format(line)
        raise ParseError(msg)
    section_name = line.strip('[]')
    return (depth, section_name.strip())


def parse_assignment(line, custom_parsers=None):
    (raw_key, raw_value) = line.split('=', 1)
    return (raw_key.strip(), parse_value(raw_value,
                                         custom_parsers=custom_parsers))

# maybe use shlex?
def parse_value(raw_value, custom_parsers=None):
    value = raw_value.strip()
    if value.startswith('[') and value.endswith(']'):
        return [parse_value(v) for v in value[1:-1].split(',')]
    elif value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    elif value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    elif value.isdigit():
        return int(value)
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    elif not value:
        return None
    elif custom_parsers:
        for (predicate, converter) in custom_parsers:
            if predicate(value):
                return converter(value)
    else:
        return value
