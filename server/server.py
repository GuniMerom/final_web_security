import bottle
import datetime
import functools
import html.parser
import json
import os
import re
import time
import base64
import model
import srvcfg
import glob
import urllib.parse



from functools import wraps
import logging






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
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def redirect_with_cookies(url, code=None, add_cookies=None, clear_cookies=None):
    if not code:
        code = 303 if bottle.request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
    res = bottle.response.copy(cls=bottle.HTTPResponse)
    for cookie in (add_cookies or ()):
        name, val = cookie
        res.set_cookie(name, val)
    for cookie in (clear_cookies or ()):
        res.delete_cookie(cookie)
    res.status = code
    res.body = ""
    res.set_header('Location', urllib.parse.urljoin(bottle.request.url, url))
    raise res

def log_to_logger(fn):
    '''
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    '''
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.datetime.now()
        actual_response = fn(*args, **kwargs)
        request = bottle.request
        response = bottle.response
        # modify this to log exactly what you need:
        logger.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        logger.info('Cookies: %s' % request.get_cookie('login'))
        logger.info('Handeled by: \'%s\' in file: \'%s\'' %(fn.__name__, SCRIPT_NAME))

        return actual_response
    return _log_to_logger



# init upload folder
if not os.path.exists(UPLOAD_DIR):
	os.makedirs(UPLOAD_DIR)

app = bottle.Bottle()
bottle.TEMPLATE_PATH.append(os.path.join(ROOT_DIR, 'views'))
app.install(log_to_logger)



def db_required(function):
    """
    Make the database connection available to the function as its first
    parameter.
    """
    @functools.wraps(function)
    def decorated(*args, **kwargs):
        with model.connect(DB_PATH) as connection:
            db_logic = model.DBLogic(connection)
            db_logic.initialize_db()
            return function(db_logic, *args, **kwargs)
    return decorated


def login_required(function):
    """
    Verify the login and return a login page if failed.
    Additionally, make the username and database connection available to the
    function as its first two parameters.
    """
    @db_required
    @functools.wraps(function)
    def decorated(db_logic, *args, **kwargs):

        login_cookie = bottle.request.get_cookie('login')

        login = db_logic.validate_login(login_cookie)
        if not login:
            return bottle.template('login')
        return function(login, db_logic, *args, **kwargs)
    return decorated

def admin_cookie(username):
    return username+'Yes'

def is_admin(username):
    if srvcfg.CTF_DIFFICULTY == 1:
            return True
    return bottle.request.get_cookie('isAdmin')==admin_cookie(username)

def get_is_admin_str(username):
    is_approved_admin = is_admin(username)
    admin_str = "" if is_approved_admin else "not"
    return admin_str

def admin_required(function):
    """
    Verify the user is logged in and admin.
    """
    @login_required
    @functools.wraps(function)
    def decorated(username, db_logic, *args, **kwargs):
        if not is_admin(username):
               return bottle.template("not_admin")
        return function(username, db_logic, *args, **kwargs)
    return decorated

def not_admin_required(function):
    """
    Verify the user is logged in and not admin. print error if yes
    """
    @login_required
    @functools.wraps(function)
    def decorated(username, db_logic, *args, **kwargs):
        if is_admin(username):
               return bottle.template("already_admin")
        return function(username, db_logic, *args, **kwargs)
    return decorated


@app.get('/enable_admin')
@not_admin_required
def view_admin_page(username, db_logic):
	return bottle.template('enable_admin')

@app.post('/enable_admin')
@not_admin_required
def view_admin_page(username, db_logic):
        cookies_ = None

        ok, had_error, query, bad_token_str = db_logic.admin_login(
            bottle.request.POST.get('password'),
        )
        if had_error:
            if srvcfg.CTF_DIFFICULTY == 2:
                return bottle.template('generic_str', str_=query)
            if srvcfg.CTF_DIFFICULTY == 3:
                return bottle.template('generic_str', str_=bad_token_str)
            if srvcfg.CTF_DIFFICULTY == 4:
                raise Exception(query)
        if ok:
            # also here cookie should be sent using bottle.response.set_cookie('login', cookie)
            # but redirect in jquery doesn't work
            cookies_ = [('isAdmin',admin_cookie(username))]
        return redirect_with_cookies('/', add_cookies=cookies_)


@app.post('/login')
@db_required
def login(db_logic):
    ok, cookie = db_logic.login(
        bottle.request.POST.get('username'),
        bottle.request.POST.get('password'),
    )
    cookies_=None
    if ok:
        bottle.response.set_cookie('login', cookie) # doesn't work - need to redirect at jquery
        cookies_=[('login',cookie)]
#    return bottle.HTTPResponse(status=200, body="you logged in you will be redirected")

#    return "you logged in you will be redirected"
#    return index(bottle.request.POST.get('username'),db_logic)
    return redirect_with_cookies('/', add_cookies=cookies_)

@app.get('/display')
@admin_required
def display_file(username, db_logic):
    fname = bottle.request.query['fname']
    fname = os.path.split(fname)[1] # only in current directory

    fpath = os.path.join(ROOT_DIR, fname)
    try :
        with open(fpath, 'rb') as f:
            return bottle.template('generic_str', str_=f.read())
    except FileNotFoundError:
        return bottle.template('generic_str', str_="File not found")
    except Exception as e:
        return bottle.template('generic_str', str_="Display ran into unknown error :(")


@app.get('/view_logs')
@admin_required
def download_newest(username, db_logic):
    
    return bottle.redirect('/display?fname=' + LOG_FILE_BASENAME)

@app.get('/logout')
def logout():
    #bottle.response.delete_cookie('login')
    delete_cookie = ['login', 'isAdmin']
    return redirect_with_cookies('/', clear_cookies=delete_cookie)


def format_timestamp(timestamp):
    date = datetime.datetime.fromtimestamp(int(timestamp))
    return date.strftime('%d.%m.%Y %H:%M:%S')


@app.get('/stats')
@login_required
def get_stats(username, db_logic):
	fcount = len(os.listdir(UPLOAD_DIR))

	return bottle.template('stats', fcount=fcount)

# logic to prevent path traversal 
def is_filename_safe(fname):
    if fname[0:2] == ".." or fname[0:4] == "./..":
        return False
    return True

@app.get('/upload')
@login_required
def get_upload(username, db_logic):
    return bottle.template('upload', username=username)

@app.post('/upload', method='POST')
@login_required
def do_upload(username, db_logic):
    request = bottle.request

    upload = request.files.get('upload')
    if not is_filename_safe(upload.filename):
        return bottle.template('generic_str', str_="Traversal attempt detected")
    upload_path = os.path.join(UPLOAD_DIR, upload.filename)
    try:
        upload.save(upload_path) 
    except Exception as e:
        return bottle.template('generic_str', str_="An error has occured. Error: %s" % e)

    # this returns full path, can be changed to basepath only
    return bottle.template('generic_str', str_="File successfully saved to '{0}'.".format(upload_path))


@app.get('/')
@login_required
def index(username, db_logic):
    name = db_logic.get_user_name(username)
    admin_str = get_is_admin_str(username)
    return bottle.template('index', name=name, username=username, is_admin_str=admin_str)

@app.get('/static/<filename:path>')
def static_resources(filename):
    return bottle.static_file(filename, root=STATIC_DIR)


def run():
    ''' 
    TODO:
    to support https
    https://stackoverflow.com/questions/44013107/how-to-make-bottle-server-https-python
    '''
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
