import os

from discord import Client

from .language import Language

class CmClient(Client):
    ENV_VARIABLE = 'CM_DISCORD_TOKEN_PATH'

    def __init__(self):
        super().__init__()
        self._lang = Language('lang/default.json')

    def token(self):
        var = CmClient.ENV_VARIABLE
        if var not in os.environ:
            raise Exception('env variable `{}` not set'.format(var))
        path = os.environ[var]

        with open(path, 'r') as fin:
            return fin.read()

    async def on_ready(self):
        print(self._lang.greet)

    async def on_message(self, message):
        if message.author == self.user:
            return

def main():
    client = CmClient()
    token = client.token()
    client.run(token)

if __name__ == '__main__':
    main()
