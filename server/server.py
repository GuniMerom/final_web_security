import bottle
import functools
import logging
import os
import srvcfg

import config
import helpers


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SCRIPT_NAME = os.path.split(__file__)[1]
DB_PATH = os.path.join(ROOT_DIR, 'db.sqlite3')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
UPLOAD_DIR = os.path.join(ROOT_DIR,'keys')
LOG_FILE_BASENAME = 'myapp.log'
LOG_FILE = os.path.join(ROOT_DIR, LOG_FILE_BASENAME)
ADMIN_USERNAME = 'admin'

# set up the logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

# init upload folder
if not os.path.exists(UPLOAD_DIR):
	os.makedirs(UPLOAD_DIR)

app = bottle.Bottle()
bottle.TEMPLATE_PATH.append(os.path.join(ROOT_DIR, 'views'))
app.install(helpers.make_app_logger(logger, __file__))


def login_required(function):
    """
    Verify the login and return a login page if failed.
    Additionally, make the username and database connection available to the
    function as its first two parameters.
    """
    @functools.wraps(function)
    @helpers.context_wrapper(db_path=DB_PATH)
    def decorated(context, *args, **kwargs):
        login_cookie = bottle.request.get_cookie(login_cookie_name())
        login = context.db_logic.validate_login(login_cookie)
        if not login:
            return context.render_template('login')
        context.username = login
        context.is_admin = is_admin(login)
        return function(context, *args, **kwargs)
    return decorated

def admin_cookie_name():
    return config.get()['admin_cookie']

def login_cookie_name():
    return config.get()['login_cookie']

def admin_cookie(username):
    return username+'Yes'

def is_admin(username):
    if srvcfg.CTF_DIFFICULTY < 2:
        return True
    return bottle.request.get_cookie(admin_cookie_name())==admin_cookie(username)

def admin_required(function):
    """
    Verify the user is logged in and admin.
    """
    @login_required
    @functools.wraps(function)
    def decorated(context, *args, **kwargs):
        if not context.is_admin:
               return context.render_template('not_admin')
        return function(context, *args, **kwargs)
    return decorated

def not_admin_required(function):
    """
    Verify the user is logged in and not admin. print error if yes
    """
    @login_required
    @functools.wraps(function)
    def decorated(context, *args, **kwargs):
        if context.is_admin:
               return context.render_template('already_admin')
        return function(context, *args, **kwargs)
    return decorated


@app.get('/enable_admin')
@not_admin_required
def view_admin_page(context):
	return context.render_template('enable_admin')

@app.post('/enable_admin')
@not_admin_required
def view_admin_page(context):
    context.debug = True
    cookies_ = None

    if context.db_logic.admin_login(
        bottle.request.POST.get('password'),
    ):
        cookies_ = [(admin_cookie_name(), admin_cookie(context.username))]
    return helpers.redirect_with_cookies('/', add_cookies=cookies_)


@app.post('/login')
@helpers.context_wrapper(db_path=DB_PATH)
def login(db_logic):
    ok, cookie = db_logic.login(
        bottle.request.POST.get('username'),
        bottle.request.POST.get('password'),
    )
    cookies_=None
    if ok:
        cookies_=[(login_cookie_name(),cookie)]
    return helpers.redirect_with_cookies('/', add_cookies=cookies_)

@app.get('/display')
@admin_required
def display_file(context):
    fname = bottle.request.query['fname']
    fname = os.path.split(fname)[1] # only in current directory

    fpath = os.path.join(ROOT_DIR, fname)
    def result(**kwargs):
        return context.render_template('generic_str', **kwargs)
    try:
        with open(fpath, 'rb') as f:
            return result(str_=f.read())
    except FileNotFoundError:
        return result(str_='File not found')
    except Exception as e:
        return result(str_='Display ran into unknown error :(')


@app.get('/view_logs')
@admin_required
def download_newest(context):
    return bottle.redirect('/display?fname=' + LOG_FILE_BASENAME)


@app.get('/logout')
def logout():
    delete_cookie = [login_cookie_name(), admin_cookie_name()]
    return helpers.redirect_with_cookies('/', clear_cookies=delete_cookie)


@app.get('/stats')
@login_required
def get_stats(context):
	fcount = len(os.listdir(UPLOAD_DIR))

	return context.render_template('stats', fcount=fcount)


def file_name_suffix(fname):
    return os.path.splitext(fname)[-1]


# logic to prevent path traversal 
def is_filename_safe(fname):
    if fname.startswith(os.sep) or fname.startswith('.'):
        return False
    parts = fname.split(os.sep)
    depth = 0
    for part in fname.split(os.sep):
        if part == '':
            continue
        if part.startswith('..'):
            depth -= 1
            ##DOC## ... don't work on file paths in Linux (they only work in cd command)
            ##DOC## This can send people on wild effort after nothing :D
        else:
            depth += 1
            ##DOC## Can be traversed with . (doesn't go down)
        if depth < 0:
            return False
    return True


@app.get('/upload')
@login_required
def get_upload(context):
    return context.render_template('upload')


@app.post('/upload', method='POST')
@login_required
def do_upload(context):
    request = bottle.request

    def result(**kwargs):
         return context.render_template('generic_str', **kwargs)

    upload = request.files.get('upload')
    if upload is None:
        return result(str_='No "upload" file specified')

    suffix = file_name_suffix(upload.raw_filename)
    if suffix and suffix not in ('.prv', '.json', '.key', '.raw'):
        return result(str_='Invalid key file type - Expected .key/.raw/.prv/.json')

    if not is_filename_safe(upload.raw_filename):
        return result(str_='Traversal attempt detected')

    upload_path = os.path.abspath(os.path.join(UPLOAD_DIR, upload.raw_filename))

    try:
        upload.save(upload_path, overwrite=True)
    except Exception as e:
        return context.render_exception(e)

    # this returns full path, can be changed to basepath only
    return result(str_=f'File successfully saved to "{upload_path}"')


@app.get('/')
@login_required
def index(context):
    return context.render_template('index')


@app.get('/static/<filename:path>')
def static_resources(filename):
    return bottle.static_file(filename, root=STATIC_DIR)


def run():
    ##DOC## To support https see
    ##DOC## https://stackoverflow.com/questions/44013107/how-to-make-bottle-server-https-python
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()

