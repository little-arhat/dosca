# -*- coding: utf-8 -*-

import shlex
import collections
from collections import OrderedDict

try:
    from __builtin__ import reduce
except ImportError:
    from functools import reduce

class ParseError(ValueError):
    pass

def dump_section(fileobj, name, params, indent=None, level=1):
    fileobj.write(format_section_line(name, level=level))
    for (k, v) in params.iteritems():
        if type(v) == collections.OrderedDict:
            dump_section(fileobj, k, v, indent=indent, level=level+1)
        elif type(v) == list:
            for x in v:
                fileobj.write(format_value_line(k, x, indent=indent))
        else:
            fileobj.write(format_value_line(k, v, indent=indent))

def save_file(res, filename, indent=None):
    with open(filename, 'w') as fileobj:
        return save(res, fileobj, indent=indent)

def save(res, fileobj, indent=None):
    for (k, v) in res.iteritems():
        if type(v) == collections.OrderedDict:
            dump_section(fileobj, k, v, indent=indent)
        else:
            fileobj.write(format_value_line(k ,v, indent=indent))

        fileobj.write("\n")

def format_section_line(name, level=1):
    return "{0}{1}{2}\n".format("[" * level, name, "]" * level)

def format_value_line(key, value, indent=None):
    return "{0}{1} = {2}\n".format(indent if indent is not None else "",
                                   key,
                                   value if value is not None else "")

def parse_file(filename, custom_parsers=None):
    with open(filename) as fileobj:
        return parse(fileobj, custom_parsers=custom_parsers)

def parse(fileobj, custom_parsers=None):
    section_stack = []
    res = OrderedDict()
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

            reduce(dict.__getitem__, section_stack, res)[section_name] = OrderedDict()
            section_stack.append(section_name)
        elif line.startswith('#') or line.startswith(';'):
            pass
        elif '=' in line:
            (key, value) = parse_assignment(line, custom_parsers=custom_parsers)
            if key.endswith('[]'):
                try:
                    reduce(dict.__getitem__, section_stack, res)[key].append(value)
                except KeyError, e:
                     reduce(dict.__getitem__, section_stack, res)[key] = [value]
            else:
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
        content = value[1:-1]
        content = [v[:-1] if v.endswith(',') else v for v in shlex.split(content)]
        if content:
            return [parse_value(v) for v in content]
        else:
            return []
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
        return value
    else:
        return value
