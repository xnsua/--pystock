from datetime import datetime
from unittest import TestCase

from common.helper import is_today


class TestIs_today(TestCase):
    def test_is_today(self):
        self.assertTrue(is_today(datetime.now()))
        self.assertFalse(is_today(datetime.fromtimestamp(1000)))
        self.assertTrue(is_today(datetime.now().date()))
