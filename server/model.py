import base64
import contextlib
import hashlib
import sqlite3
import time
import bottle
import srvcfg



def sha1(val):
    s = hashlib.sha1()
    if isinstance(val, str):
        val = val.encode()
    s.update(val)
    return s.hexdigest()


def create_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.create_function('sha1', 1, sha1)
    return conn


@contextlib.contextmanager
def connect(db_path):
    with create_connection(db_path) as conn:
        yield conn


class DBLogic:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.initialize_db()

    def initialize_db(self):
        self.db_connection.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                user_id  INTEGER PRIMARY KEY,
                username  TEXT,
                password  TEXT,
                full_name TEXT
            );
        ''')


        self.db_connection.executescript('''
            INSERT OR IGNORE INTO users VALUES (1, 'boss', sha1('Dancing in the dark'), 'Bruce Summersteen');
            INSERT OR IGNORE INTO users VALUES (2, 'edward', sha1('666'), 'Edward Hailden');
            INSERT OR IGNORE INTO users VALUES (3, 'alice', sha1('Into the flood again.'), 'Alice InRopes');
            INSERT OR IGNORE INTO users VALUES (4, 'bob', sha1('Is this love'), 'Bob Marmite');
            INSERT OR IGNORE INTO users VALUES (5, 'system', '', 'Grape Galili');
            INSERT OR IGNORE INTO users VALUES (6, 'test', sha1('1234'), 'Testy McTestFace');
            INSERT OR IGNORE INTO users VALUES (7, 'admin', sha1('ReallyStr0nkP@ssw0rd'), 'System Administrator');
        ''')


    def select_scalar(self, *args, **kwargs):
        """Utility to return a scalar value from a query."""
        row = self.db_connection.execute(*args, **kwargs).fetchone()
        return None if row is None else row[0]

    def login(self, username, password):

        match = self.select_scalar(
            "SELECT * FROM users WHERE username = ? AND password = sha1(?)",
            (username, password,)
        )
        if match:
            return True, base64.b64encode(username.encode()).decode()
        else:
            return False, ''

    def admin_login(self, password):
        match = None
        had_error = False
        bad_token_str = ''
        query = "SELECT * FROM users where username = 'admin' AND password = sha1('%s')"%(password,)
        print("Admin login query: %s" % query)
        try:
            match = self.select_scalar(query)
        except sqlite3.OperationalError as e:
            print("raised exception: %s" % e)
            had_error = True
            bad_token_str = "%s" % e

        status = True if match else False
        return status, had_error, query, bad_token_str

    def validate_login(self, cookie):
        #logger.warning('This is only a test')

        if not cookie:
            return False
        try:
            # b64decode returns bytes, another decode to get a string
            #print("cookie: {}".format(cookie))
            login = base64.b64decode(cookie).decode()

        except:
            return False
        if self.select_scalar(
            "SELECT * FROM users WHERE username = ?",
            (login,)
        ):
            return login
        else:
            return None

    def get_user_name(self, username):
        return self.select_scalar(
            "SELECT full_name FROM users WHERE username = ?",
            (username,)
        )

    def get_user_id(self, username):
        return self.select_scalar(
            "SELECT user_id FROM users WHERE username = ?",
            (username,)
        )
