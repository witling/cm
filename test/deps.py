import pytest
import sys

from os.path import abspath, dirname, join

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from cm import *

class Test:
    def assertEqual(self, expected, got):
        assert expected == got
