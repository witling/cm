import pytest
import sys

from os.path import abspath, dirname, join

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from cm import *

@pytest.fixture
def app():
    return App()

class Test:
    def assertEqual(self, expected, got):
        assert expected == got

    def assertTrue(self, got):
        assert got
