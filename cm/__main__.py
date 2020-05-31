from .app import App
from .client import CmClient

def main():
    client = CmClient(App())
    token = client.token()
    client.run(token)

if __name__ == '__main__':
    main()
