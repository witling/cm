import pytest

from deps import *

class TestCodeRun(Test):
    def test_extracting_code(self):
        args, src = client._code_executor.extract_code("""`quasi "hej"`""")
        self.assertEqual('quasi "hej"', src)

        src = """
```
use std
```
        """
        args, src = client._code_executor.extract_code(src)

        self.assertEqual('use std', src)

    def test_extracting_link(self):
        import mistune

        link = 'https://raw.githubusercontent.com/witling/quasicode/master/examples/hello-world.qc'
        content = """[example]({})""".format(link)

        renderer = CustomRenderer()
        markdown = mistune.markdown(content, renderer=renderer)

        self.assertEqual(link, renderer._link)
