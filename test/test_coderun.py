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

    def test_extracting_link(self):
        import mistune

        link = 'https://raw.githubusercontent.com/witling/quasicode/master/examples/hello-world.qc'
        content = """[example]({})""".format(link)

        renderer = CustomRenderer()
        markdown = mistune.markdown(content, renderer=renderer)

        self.assertEqual(link, renderer._link)
