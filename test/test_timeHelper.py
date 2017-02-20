from unittest import TestCase

from common.helper import find_date_substr, search_substr_by_regex

class TestIsToday(TestCase):
    def test_find_date_substr(self):
        dstr = 'abc123'
        regex = '\d+'
        substr = search_substr_by_regex(regex, dstr)
        self.assertEqual(substr, '123')
        self.assertEqual(find_date_substr('d2011-01-1b'), '2011-01-1')
