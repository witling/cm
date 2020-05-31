from .executor import CodeExecutor
from .language import Language

class App:
    CMD_START = '$'

    def __init__(self):
        self._lang = Language.get()
        self._code_executor = CodeExecutor(self)
        self._user = None

        self._cmds = {}
        cmds = {
            'run': self._code_executor.handle,
            'help': self._help,
        }

        for cmd, callback in cmds.items():
            self._cmds[App.CMD_START + cmd] = callback

    def language(self):
        return self._lang

    def channel_topic(self):
        return '{}\n\n'.format(self._lang.channel_topic)

    def greet(self):
        return self._lang.greet

    def extract_args(self, content):
        args = []
        for word in content.split(' '):
            if word.startswith(App.CMD_START):
                continue
            if not word.startswith('--'):
                break
            args.append(word)
        return args

    async def _help(self, message):
        msg = '{}\n\n{}\n\n{}'.format(
            self._lang.channel_topic,
            self._lang.help,
            self._lang.help_command_prefix.format(App.CMD_START)
        )
        await message.channel.send(msg)

    async def dispatch(self, cmd, message):
        if cmd in self._cmds:
            await self._cmds[cmd](message)
