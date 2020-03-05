from app import db, app
# from datetime import datetime
# import random
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context




class User(db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=31536000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user



# class Register(db.Model):
#     __tablename__ = 'register'
#
#     s_n = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     pin = db.Column(db.String(140), unique=True, nullable=False)
#     request_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#     def __init__(self, pin):
#         self.pin = pin
#
#     def __repr__(self):
#         return '{}'.format(self.pin)
#
#
# def random_digits(n):
#     """ A function to generate random 15 digit number. where n is the number of Digits"""
#     lower = 10**(n-1)
#     upper = 10**n - 1
#     return random.randint(lower, upper)


# def twelve_digit_serial_no(id):
#     """ The function create a 12 digit serial number from any number with less than 11 digits"""
#     f = str(10**(11 - len(str(id))))
#     twelve_digit_id = f + str(id)
#     return int(twelve_digit_id)
#
#
# def database_serial_no(twelve_digit_sn):
#     db_id = int(twelve_digit_sn) - 10**11
#     return db_id
