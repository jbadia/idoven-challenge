from datetime import datetime
from pony import orm
from pony.orm import db_session, select, flush
from passlib.hash import sha512_crypt
from core.errors import UnprivilegedError

db = orm.Database()
USER_ROLES = ['admin', 'user']

class User(db.Entity):
    _table_ = "USERS"
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    password = orm.Required(str)
    roles = orm.Required(orm.Json)
    ecg = orm.Set("ECG")

    def __init__(self, *args, **kwargs):
        # Checking roles
        priv_match = (True if p in USER_ROLES else False for p in kwargs['roles'])
        if not all(priv_match):
            raise UnprivilegedError("Provided roles not supported")

        # Encrypt password
        kwargs['password'] = User.encrypt_password(kwargs['password']) if 'password' in kwargs else None

        super(User, self).__init__(*args, **kwargs)

    def verify_password(self, password: str) -> bool:
        return sha512_crypt.verify(password, self.password)
    
    @staticmethod
    def encrypt_password(password: str):
        return sha512_crypt.encrypt(password)


class ECG(db.Entity):
    _table_ = "ECG"
    id = orm.PrimaryKey(str, max_len=200)
    user = orm.Required(User)
    date = orm.Required(datetime)
    leads = orm.Set("ECGLeads")


class ECGLeads(db.Entity):
    _table_ = "ECG_LEADS"
    ecg = orm.Required(ECG)
    name = orm.Required(str)
    num_samples = orm.Optional(int)
    signal = orm.Required(orm.Json)
    count_zero_crossings = orm.Optional(int)


select = select
db_session = db_session
flush = flush