import enum
import io
import mistune

from qclib import Compiler, Interpreter

@enum.unique
class MessageState(enum.Enum):
    PROCESSING = '\N{CLOCK FACE ONE OCLOCK}'
    DONE = '\N{WHITE HEAVY CHECK MARK}'
    ERROR = '\N{CROSS MARK}'

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

    async def set_message_state(self, message, state):
        await message.add_reaction(state.value)
        
        # TODO: remove other reactions if there are any

    async def handle(self, message):
        content = message.content

        await self.set_message_state(message, MessageState.PROCESSING)

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
