import bottle
import datetime
import functools
import model
import os
import srvcfg
import urllib.parse
import traceback


def redirect_with_cookies(url, code=None, add_cookies=None, clear_cookies=None):
    if not code:
        code = 303 if bottle.request.get('SERVER_PROTOCOL') == 'HTTP/1.1' else 302
    res = bottle.response.copy(cls=bottle.HTTPResponse)
    for cookie in (add_cookies or ()):
        name, val = cookie
        res.set_cookie(name, val)
    for cookie in (clear_cookies or ()):
        res.delete_cookie(cookie)
    res.status = code
    res.body = ''
    res.set_header('Location', urllib.parse.urljoin(bottle.request.url, url))
    raise res


def make_app_logger(logger, filename):
    SCRIPT_NAME = os.path.split(filename)[1]
    def decorator(fn):
        """
        Wrap a Bottle request so that a log line is emitted after it's handled.
        (This decorator can be extended to take the desired logger as a param.)
        """
        @functools.wraps(fn)
        def result(*args, **kwargs):
            request_time = datetime.datetime.now()
            actual_response = fn(*args, **kwargs)
            request = bottle.request
            response = bottle.response
            # modify this to log exactly what you need:
            logger.info('%s %s %s %s %s', request.remote_addr,
                                          request_time,
                                          request.method,
                                          request.url,
                                          response.status)
            logger.info('Cookies: %s', request.get_cookie('login'))
            logger.info('Handeled by: "%s" in file: "%s"', fn.__name__, SCRIPT_NAME)

            return actual_response
        return result
    return decorator


class Context:
    def __init__(self, db_logic):
        self.db_logic = db_logic
        self.username = None
        self.is_admin = None
        self.debug = False

    @property
    def is_logged_in(self):
        return self.username is not None and self.db_logic

    def render_template(self, tmpl_name, **kwargs):
        params = dict(kwargs)
        if self.is_logged_in:
            params['username'] = self.username
            params['name'] = self.db_logic.get_user_name(self.username)
            params['is_admin'] = self.is_admin
        return bottle.template(tmpl_name, **params)

    def render_exception(self, e):
        trace = traceback.format_exc()
        return self.render_template('error', title=type(e).__name__, value=trace)

def context_wrapper(*, db_path, debug=False):
    def wrapper(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            with model.connect(db_path) as connection:
                context = Context(db_logic=model.DBLogic(connection))
                context.db_logic.initialize_db()
            context.debug = debug
            try:
                return func(context, *args, **kwargs)
            # Bottle returns all responses via Exceptions. Yuck :(
            except bottle.HTTPResponse:
                raise
            # Format real exceptions.
            except Exception as e:
                if not context.debug or srvcfg.CTF_DIFFICULTY >= 3:
                    raise
                return context.render_exception(e)
        return result
    return wrapper
