import pytest

from deps import *

class TestUtil(Test):
    def test_trimming_command(self):
        self.assertEqual('abc', CmClient.strip_command('$run abc'))
        self.assertEqual('quasi "test"', CmClient.strip_command(' $run quasi "test"'))

        self.assertEqual('coding', CmClient.strip_command('$help coding'))
        self.assertEqual('coding', CmClient.strip_command('  $help   coding'))
