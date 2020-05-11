import os

from discord import Client

from .executor import CodeExecutor
from .language import Language

class CmClient(Client):
    ENV_VARIABLE = 'CM_DISCORD_TOKEN_PATH'
    CMD_START = '$'

    def __init__(self):
        super().__init__()
        self._lang = Language.get()
        self._channel = None
        self._code_executor = CodeExecutor(self)

        self._cmds = {}
        cmds = {
            'run': self._code_executor.handle
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

    def language(self):
        return self._lang

    async def on_ready(self):
        if self._channel is None:
            self._channel = self.search_channel()

            await self._channel.edit(topic=self._lang.channel_topic)
        await self._channel.send(self._lang.greet)

    async def on_message(self, message):
        if message.author == self.user:
            return

        parts = message.content.split()
        if parts[0] in self._cmds:
            await self._cmds[parts[0]](message)

