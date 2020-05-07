import io
import mistune

from qclib import Compiler, Interpreter

class CustomRenderer(mistune.Renderer):
    def __init__(self):
        super().__init__()
        self._code = None

    def code(self):
        return self._code

    def codespan(self, code):
        self._code = code
        return code

    def block_code(self, code, lang=None):
        self._code = code
        return code

class CodeExecutor:
    def __init__(self):
        self._compiler = Compiler()

    def extract_code(content):
        renderer = CustomRenderer()
        markdown = mistune.markdown(content, renderer=renderer)
        if not renderer.code() is None:
            return renderer.code()
        return content

    def handle(self, content):
        src = CodeExecutor.extract_code(content)
        if src is None:
            raise Exception('format was invalid')

        stdout = io.StringIO()
        program = self._compiler.compile(src)

        interpreter = Interpreter()
        interpreter._ctx.set_stdout(stdout)

        interpreter.load(program)
        interpreter.run()

        return stdout.getvalue()
