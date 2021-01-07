import os


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
