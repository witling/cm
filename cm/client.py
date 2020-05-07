import os
import re

from discord import Client

from .executor import CodeExecutor
from .language import Language

class CmClient(Client):
    ENV_VARIABLE = 'CM_DISCORD_TOKEN_PATH'
    CMD_START = '$'

    def __init__(self):
        super().__init__()
        self._lang = Language('lang/default.json')
        self._channel = None
        self._code_executor = CodeExecutor()

        self._cmds = {}
        cmds = {
            'run': self._run_code
        }

        for cmd, callback in cmds.items():
            self._cmds[CmClient.CMD_START + cmd] = callback

    def token(self):
        var = CmClient.ENV_VARIABLE
        if var not in os.environ:
            raise Exception('env variable `{}` not set'.format(var))
        path = os.environ[var]

        with open(path, 'r') as fin:
            return fin.read()

    def search_channel(self):
        for server in self.guilds:
            for channel in server.text_channels:
                if channel.name == 'quasicoding':
                    return channel
        return None

    def strip_command(content):
        match = re.match('^(\s*\$\S+)', content)
        if match is None:
            return

        cut = len(match.group(1))
        return content[cut:].strip()

    async def _run_code(self, message):
        try:
            content = CmClient.strip_command(message.content)
            output = self._code_executor.handle(content)
            await message.channel.send(output)

        except Exception as e:
            msg = '{}\n{}'.format(self._lang.buggy_code_given, e)
            await message.channel.send(msg)

    async def on_ready(self):
        if self._channel is None:
            self._channel = self.search_channel()

            await self._channel.edit(topic=self._lang.channel_topic)
        await self._channel.send(self._lang.greet)

    async def on_message(self, message):
        if message.author == self.user:
            return

        parts = message.content.split(' ')
        if parts[0] in self._cmds:
            await self._cmds[parts[0]](message)

