from datetime import datetime
from unittest import TestCase

from common.string_helper import search_substr_by_regex
from common.time_helper import is_today, find_date_substr


class TestIsToday(TestCase):
    def test_is_today(self):
        self.assertTrue(is_today(datetime.now()))
        self.assertFalse(is_today(datetime.fromtimestamp(1000)))
        self.assertTrue(is_today(datetime.now().date()))

    def test_find_date_substr(self):
        dstr = 'abc123'
        regex = '\d+'
        substr = search_substr_by_regex(dstr, regex)
        self.assertEqual(substr, '123')
        self.assertEqual(find_date_substr('d2011-01-1b'), '2011-01-1')
