import re

def search_substr_by_regex(source: str, regex: str):
    reg = re.compile(regex)
    match = reg.search(source)
    return match.group()



