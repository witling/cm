import pytest

from deps import *

class TestUtil(Test):
    def test_trimming_command(self):
        self.assertEqual('abc', strip_command('$run abc'))
        self.assertEqual('quasi "test"', strip_command(' $run quasi "test"'))

        self.assertEqual('coding', strip_command('$help coding'))
        self.assertEqual('coding', strip_command('  $help   coding'))
