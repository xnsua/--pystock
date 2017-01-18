import re


def search_substr_by_regex(source: str, regex: str):
    reg = re.compile(regex)
    match = reg.search(source)
    return match.group()


def find_date_substr(source: str):
    return search_substr_by_regex(source, '\d{4}-\d{1,2}-\d{1,2}')


if __name__ == '__main__':
    str = 'abc123'
    regex = '\d+'
    substr = search_substr_by_regex(str, regex)
    assert substr == '123'
    assert find_date_substr('d2011-01-1b') == '2011-01-1'
