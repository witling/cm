import enum
import io
import mistune
import re

from qclib import Compiler, Interpreter

from .util import strip_command

def read_source_from_url(url):
    from urllib.request import urlopen
    response = urlopen(url)
    print(response.info())
    return response.read().decode('utf-8')

@enum.unique
class MessageState(enum.Enum):
    PROCESSING = '\N{CLOCK FACE ONE OCLOCK}'
    DONE = '\N{WHITE HEAVY CHECK MARK}'
    ERROR = '\N{CROSS MARK}'

class CustomRenderer(mistune.Renderer):
    def __init__(self):
        super().__init__()
        self._code = None
        self._link = None

    def link(self, link, title, text):
        self._link = link
        return self._link

    def code(self):
        if not self._link is None:
            return read_source_from_url(self._link)
        return self._code

    def codespan(self, code):
        self._code = code
        return code

    def block_code(self, code, lang=None):
        self._code = code
        return code

class CodeExecutor:
    RE_URL = re.compile('(www|http)\S+')
    ERR_DIRECTORY = 'errors'

    def __init__(self, client):
        self._client = client
        self._compiler = Compiler()

    def extract_code(content):
        # try to interpret message as link first
        url_match = CodeExecutor.RE_URL.match(content)
        if url_match:
            link = url_match.group(0)
            return read_source_from_url(link)
        
        else:
            renderer = CustomRenderer()
            markdown = mistune.markdown(content, renderer=renderer)
            if not renderer.code() is None:
                return renderer.code()

        return content

    def _backup_error_src(self, src):
        import datetime
        import os

        try:
            os.mkdir(CodeExecutor.ERR_DIRECTORY)
        except:
            pass

        n = datetime.datetime.now()
        fpath = os.path.join(CodeExecutor.ERR_DIRECTORY, '{}.qc'.format(n.isoformat()))
        with open(fpath, 'w') as fout:
            fout.write(src)

    async def set_message_state(self, message, state):
        for reaction in message.reactions:
            await reaction.remove(self._client.user)

        await message.add_reaction(state.value)

    async def process(self, message):
        content = message.content

        await self.set_message_state(message, MessageState.PROCESSING)

        src = CodeExecutor.extract_code(content)
        if src is None:
            raise Exception(self._client.language().invalid_message_format)

        try:
            if not src:
                raise Exception(self._client.language().no_code_to_run)

            stdout = io.StringIO()
            program = self._compiler.compile(src, auto_main=True)

            interpreter = Interpreter(restricted=True)
            interpreter._ctx.set_stdout(stdout)
            interpreter._ctx.set_allowed_modules(['std', 'string'])

            interpreter.load(program)
            interpreter.run()

            return stdout.getvalue()

        except Exception as e:
            self._backup_error_src(src)
            raise e

    async def handle(self, message):
        try:
            message.content = strip_command(message.content)
            output = await self.process(message)

            await message.channel.send('{}\n {}'.format(message.author.mention, output))
            await self.set_message_state(message, MessageState.DONE)

        except Exception as e:
            msg = '{}\n{}'.format(self._client.language().buggy_code_given, e)

            await message.channel.send('{}\n {}'.format(message.author.mention, msg))
            await self.set_message_state(message, MessageState.ERROR)
