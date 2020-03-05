from app import app, db, mongo, auth
from flask import jsonify, request, abort, url_for, g
from app.models import User #Register, random_digits
# , twelve_digit_serial_no

# @app.route('/generate', methods=['GET'])
# def generate():
#
#     mongo_data = mongo.db.voucher
#
#     # implemnting while loop to ensure that the random generated pin doesn't already exist in the database
#     counter = 1
#     while counter >= 1:
#         pin = random_digits(15)
#         pin1 = mongo_data.find_one({'pin': pin})
#
#         if pin1:
#             print('again')
#             counter = counter + 1
#         else:
#             print(pin)
#             break
#
#     save = Register(pin=str(pin))
#     db.session.add(save)
#     db.session.commit()
#     serial_number = Register.query.filter_by(pin=str(pin)).first()
#     pin1 = pin
#     # sn = twelve_digit_serial_no(serial_number.s_n)
#     sns = serial_number.s_n
#     sn = '%012d' % sns
#     # storing to mongo db
#     mongo_data.insert({'serial_no': int(sn), 'pin': pin1, 'activation_status': 0, 'dealer_id':122445, 'batch':40})
#
#     return jsonify({'serial number': sn, 'PIN': pin1})
#

@app.route('/', methods=['GET'])
def index():
    msg = "Welcome!, with this API you can activate or deactivate cards specifying the serial number and category (range) of the card(s) N.B: only assigned cards can be activated!!!, and only activated cards can be deactivated  <<HAPPY TESTING>>!"
    return jsonify({"Message": msg})




@app.route('/api/users', methods=['POST'])
def new_user():
    mongo_data = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) #missing arguements
    if User.query.filter_by(username = username).first() is not None:
        abort(400) #existing user

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    mongo_data.insert({"username": username, "password":password})
    return jsonify({" Registered successful. username": user.username}), 201, {"Location": url_for('new_user', id = user.id, _external=True)}

# @app.route('/api/resource')
# @auth.login_required
# def get_resource():
#     return jsonify({'data': 'hello, %s!' % g.user.username})

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'API_KEY': token.decode('ascii') })





@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            "Message":"Sorry the page your are looking for is not here kindly go back"
        },
        {
            "status": 404
        }
    )


@app.errorhandler(400)
def bad_request__error(error):
    return jsonify(
        {
            "Message": "Sorry you entered wrong values kindly check and resend!"
        },
        {
            "status":400
        }
    )

@app.errorhandler(500)
def internal_error(error):
    return jsonify(
        {
            "Message": "Sorry some errors has occured the administrator has been notified meanwhile kindly check if you specified all parameters accordinly"
        },
        {
            "status": 500
        }
    )

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Sorry the requested method is not allowed kindly check and resend !"
        },
        {
            "status": 405
        }
    )