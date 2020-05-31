import pytest

from deps import *

class TestCodeRun(Test):
    def test_extracting_single_code(self, app):
        args, src = app._code_executor.extract_code("""`quasi "hej"`""")
        self.assertTrue(args['funny_mode'])
        self.assertEqual('quasi "hej"', src)

    def test_extracting_block_code(self, app):
        src = """
```
use std
```
        """
        args, src = app._code_executor.extract_code(src)

        self.assertEqual('use std', src)

    def test_disable_funny_mode(self, app):
        args, src = app._code_executor.extract_code('--nichluschdich `quasi "hej"`')
        self.assertTrue(not args['funny_mode'])
        self.assertEqual('quasi "hej"', src)

    def test_extracting_link(self):
        import mistune

        link = 'https://raw.githubusercontent.com/witling/quasicode/master/examples/hello-world.qc'
        content = """[example]({})""".format(link)

        renderer = CustomRenderer()
        markdown = mistune.markdown(content, renderer=renderer)

        self.assertEqual(link, renderer._link)
