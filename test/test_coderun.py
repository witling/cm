import pytest

from deps import *

class TestCodeRun(Test):
    def test_extracting_code(self):
        self.assertEqual('quasi "hej"', CodeExecutor.extract_code("""`quasi "hej"`"""))

        src = """
```
use std
```
        """

        self.assertEqual('use std', CodeExecutor.extract_code(src))
