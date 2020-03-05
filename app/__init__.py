from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_pymongo import PyMongo
from datetime import datetime, date
from flask_httpauth import HTTPBasicAuth

# from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mongo = PyMongo(app)
auth = HTTPBasicAuth()

def cur_time_and_date():
    now = datetime.utcnow()
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S")
    return (d2 +' '+'at'+' '+tm)

# The actual decorator function
# def require_appkey(view_function):
#     @wraps(view_function)
#     # the new, post-decoration function. Note *args and **kwargs here.
#     def decorated_function(*args, **kwargs):
#         if request.args.get('key') and request.args.get('key') == '0987654321234567890':
#             return view_function(*args, **kwargs)
#         else:
#             return jsonify(
#                 {
#                     "Message": "Please supply API KEY to continue"
#                 },
#                 {
#                     "Status": 401
#                 }
#             )
#     return decorated_function



from app import route, models, deactivate, activate