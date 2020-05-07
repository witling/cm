from discord import Client
import os

class CmClient(Client):
    ENV_VARIABLE = 'CM_DISCORD_TOKEN_PATH'

    def token(self):
        var = CmClient.ENV_VARIABLE
        if var not in os.environ:
            raise Exception('env variable `{}` not set'.format(var))
        path = os.environ[var]

        with open(path, 'r') as fin:
            return fin.read()

    def run(self):
        token = self.token()
        super().run(token)

def main():
    client = CmClient()
    client.run()
