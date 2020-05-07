import io

from qclib import Compiler, Interpreter

class CodeExecutor:
    def __init__(self):
        self._compiler = Compiler()

    def _extract_code(self, content):
        return content

    def handle(self, content):
        stdout = io.StringIO()
        src = self._extract_code(content)
        program = self._compiler.compile(src)

        interpreter = Interpreter()
        interpreter._ctx.set_stdout(stdout)

        interpreter.load(program)
        interpreter.run()

        return stdout.getvalue()
