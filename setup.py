import os


SECRET_TOKEN = '##DOC##'


def strip_secrets(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    if SECRET_TOKEN not in data:
        return
    print('Stripping %s' % path)
    clean_lines = []
    for line in data.splitlines():
        if SECRET_TOKEN in line:
            new_line = line.split(SECRET_TOKEN, 1)[0].rstrip()
            if new_line:
                clean_lines.append(new_line)
        else:
            clean_lines.append(line)
    new_data = os.linesep.join(clean_lines)
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(new_data)
    os.replace(tmp_path, path)


def strip_secrets_from_files(root):
    for root, dirs, files in os.walk(root):
        for f in files:
            if f.endswith('.py'):
                strip_secrets(os.path.join(root, f))


def setup():
    try:
        import bottle
        return
    except:
        # Bottle is not installed
        pass

    print('Running installation below, you might be prompted for sudo password')
    os.system('sudo apt install -q -y python3-bottle')


if __name__ == '__main__':
    setup()
    server_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'server')
    strip_secrets_from_files(server_dir)
