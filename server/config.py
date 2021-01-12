import datetime
import json


CONFIG_ = None
LAST_LOAD_ = None
DEFAULT_CONFIG_ = {
    'Example': True
}


def maybe_reload_(path):
    import os
    global LAST_LOAD_
    try:
        if not os.path.isfile(path):
            print('No config file')
            return
        ts = os.stat(path).st_mtime
        if LAST_LOAD_ is None or ts > LAST_LOAD_:
            print('Fresh time, reloading')
            LAST_LOAD_ = ts
            reload_(path)
    except:
        print('Exception')
        pass


def get():
    maybe_reload_(config_path_())
    result = dict(DEFAULT_CONFIG_)
    # Use overrides from the file
    if CONFIG_:
        result.update(CONFIG_)
    return result


def config_path_():
    import os
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'config.json')

def reload_(path):
    global CONFIG_
    print('New timestamp %s' % LAST_LOAD_)
    with open(path, 'r') as f:
        CONFIG_ = eval(f.read())
    print(f'Reloaded config - {json.dumps(CONFIG_)}')
