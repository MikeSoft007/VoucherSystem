# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
# from flask import request, jsonify, abort, url_for, g
# from passlib.apps import custom_app_context as pwd_context
# from app import db, app
# from flask_httpauth import HTTPBasicAuth
#
# auth = HTTPBasicAuth()
#
# class User(db.Model):
#     __tablename__ ='users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(32), index=True)
#     password_hash = db.Column(db.String(128))
#
#     def hash_password(self, password):
#         self.password_hash = pwd_context.encrypt(password)
#
#     def verify_password(self, password):
#         return pwd_context.verify(password, self.password_hash)
#
#     def generate_auth_token(self, expiration=31536000):
#         s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
#         return s.dumps({'id': self.id})
#
#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None  # valid token, but expired
#         except BadSignature:
#             return None  # invalid token
#         user = User.query.get(data['id'])
#         return user
#
# @app.route('/api/users', methods=['POST'])
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         abort(400) #missing arguements
#     if User.query.filter_by(username = username).first() is not None:
#         abort(400) #existing user
#
#     user = User(username=username)
#     user.hash_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"username": user.username}), 201, {"Location": url_for('new_user', id = user.id, _external=True)}
#
# # @app.route('/api/resource')
# # @auth.login_required
# # def get_resource():
# #     return jsonify({'data': 'hello, %s!' % g.user.username})
#
# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username = username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True
#
#
# @app.route('/api/token')
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify({'API_KEY': token.decode('ascii') })
