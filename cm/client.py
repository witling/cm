import os

from discord import Client

from .app import App

class CmClient(Client):
    ENV_VARIABLE = 'CM_DISCORD_TOKEN_PATH'

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._channel = None

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

    async def on_ready(self):
        self._app._user = self.user
        
        if self._channel is None:
            self._channel = self.search_channel()
            await self._channel.edit(topic=self._app.channel_topic())

        await self._channel.send(self._app.greet())

    async def on_message(self, message):
        if message.author == self.user:
            return

        parts = message.content.split()
        await self._app.dispatch(parts[0], message)
