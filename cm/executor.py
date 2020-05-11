import enum
import io
import mistune

from qclib import Compiler, Interpreter

from .util import strip_command

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
    def __init__(self, client):
        self._client = client
        self._compiler = Compiler()

    def extract_code(content):
        renderer = CustomRenderer()
        markdown = mistune.markdown(content, renderer=renderer)
        if not renderer.code() is None:
            return renderer.code()
        return content

    async def set_message_state(self, message, state):
        for reaction in message.reactions:
            await reaction.remove(self._client.user)

        await message.add_reaction(state.value)

    async def process(self, message):
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

    async def handle(self, message):
        try:
            message.content = strip_command(message.content)
            output = await self.process(message)

            await message.channel.send(output)
            await self.set_message_state(message, MessageState.DONE)

        except Exception as e:
            msg = '{}\n{}'.format(self._client.language().buggy_code_given, e)

            await message.channel.send(msg)
            await self.set_message_state(message, MessageState.ERROR)
