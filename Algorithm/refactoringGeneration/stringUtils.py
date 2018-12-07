import re
from re import finditer

NAME_LENGTH = 5
DEFAULT_NAME = "*"


def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def tokenize_name(name):
    if name.startswith("_"):
        name = name.substring(1)
    if name.upper() == name:
        tokenized_string = re.compile("_").split(name)
    else:
        tokenized_string = camel_case_split(name)
    return list(map(lambda token: token.lower(), tokenized_string))


def partition_name(name):
    tokenized_name = tokenize_name(name)
    to_skip = NAME_LENGTH - min(len(tokenized_name), NAME_LENGTH)
    partitioned_name = list()
    for i in range(NAME_LENGTH):
        partitioned_name.append(tokenized_name[i - to_skip] if 0 <= i - to_skip else DEFAULT_NAME)
    return partitioned_name
