# -*- coding: utf-8 -*-

__all__ = ('parse', 'parse_file', 'ParseError')


class ParseError(ValueError):
    pass


def parse_file(filename):
    with open(filename) as fileobj:
        return parse(fileobj)


def parse(fileobj):
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
            for _ in xrange(diff):
                section_stack.pop()

            reduce(dict.__getitem__, section_stack, res)[section_name] = {}
            section_stack.append(section_name)
        elif line.startswith('#'):
            pass
        elif '=' in line:
            (key, value) = parse_assignment(line)
            reduce(dict.__getitem__, section_stack, res)[key] = value
        else:
            raise ParseError('Unrecognized line: `{}`'.format(line))
    return res


def parse_section(line):
    depth = line.count('[')
    if depth != line.count(']'):
        msg = 'Unbalanced brackets in section definition: `{}`'.format(line)
        raise ParseError(msg)
    section_name = line.strip('[]')
    return (depth, section_name.strip())


def parse_assignment(line):
    (raw_key, raw_value) = line.split('=', 1)
    return (raw_key.strip(), parse_value(raw_value))

# maybe use shlex?
def parse_value(raw_value):
    value = raw_value.strip()
    if value.startswith('[') and value.endswith(']'):
        return map(parse_value, value[1:-1].split(','))
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
    else:
        return value