import datetime
import json
import srvcfg


CONFIG_ = None
LAST_LOAD_ = None
DEFAULT_CONFIG_ = {
    'login_cookie': 'login',
    'admin_cookie': 'isAdmin',
}


def maybe_reload_(path):
    import os
    global LAST_LOAD_
    try:
        if not os.path.isfile(path):
            return
        ts = os.stat(path).st_mtime
        if LAST_LOAD_ is None or ts > LAST_LOAD_:
            LAST_LOAD_ = ts
            reload_(path)
    except:
        pass


def get():
    maybe_reload_(config_path_())
    result = dict(DEFAULT_CONFIG_)
    # Use overrides from the file
    if CONFIG_:
        result.update(CONFIG_)
    return result


def reload_(path):
    global CONFIG_
    with open(path, 'r') as f:
        CONFIG_ = eval(f.read())


##DOC## Intentionally have os in the scope for eval in low levels.
##DOC## In tougher levels, don't have OS available.
##DOC## Hide this by supposedly changing a function, to not have a big if around
##DOC## an import statement (that's a big bad hint).
if srvcfg.CTF_DIFFICULTY < 4:
    import os
    def config_path_():
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'config.json')
else:
    def config_path_():
        return 'config.json'

