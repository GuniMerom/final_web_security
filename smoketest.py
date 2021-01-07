import os

from infosec.utils import smoke, SmoketestFailure


@smoke.smoke_check
def check_msg(path):
    with open(path, 'r') as f:
        header = f.readline()
        if not header.startswith('#'):
            smoke.error(f'First line of {path} should be a channel name and '
                        f'begin with a #')
            return
        if not f.read().strip():
            smoke.error(f'No content provided (after the channel) in {path}')
            return
    smoke.success(f'{path} seems cool')


@smoke.smoke_check
def make_check(prefix):
    console_path = prefix + '.console'
    msg_path = prefix + '.msg'
    txt_path = prefix + '.txt'
    if os.path.exists(console_path) and os.path.exists(msg_path):
        smoke.error(f'Provided both {console_path} and {msg_path}')
    elif os.path.exists(console_path):
        smoke.check_if_nonempty(console_path)
    elif os.path.exists(msg_path):
        check_msg(msg_path)
    else:
        smoke.error(f"Couldn't find {console_path} or {msg_path}")


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    smoke.check_if_nonempty('q1.console')
    smoke.check_if_nonempty('q1.txt')

    make_check('q2')
    smoke.check_if_nonempty('q2.txt')

    make_check('q3')
    smoke.check_if_nonempty('q3.txt')

    make_check('q4')
    smoke.check_if_nonempty('q4.txt')

    smoke.check_if_nonempty('q5.html')
    smoke.check_if_nonempty('q5.txt')


if __name__ == '__main__':
    smoketest()
