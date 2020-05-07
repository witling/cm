from .client import CmClient

def main():
    client = CmClient()
    token = client.token()
    client.run(token)

if __name__ == '__main__':
    main()
