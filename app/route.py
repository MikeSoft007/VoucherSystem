from app import app, db, mongo, auth
from flask import jsonify, request, abort, url_for, g
from app.models import User
# , Register, random_digits #, twelve_digit_serial_no
from passlib.apps import custom_app_context as pwd_context


@app.route('/', methods=['GET'])
def index():
    try:
        msg = " Hello Welcome!, First register and sign in to generate your API KEY as specified the the documentation, With this API you can activate or deactivate cards specifying the serial number and category (range) of the card(s) N.B: only assigned cards can be activated!!!, and only activated cards can be deactivated  <<HAPPY TESTING>>!"
        return jsonify({"Message": msg})
    except Exception:
        abort(500)




@app.route('/api/users', methods=['POST'])
def new_user():
    try:
        mongo_data = mongo.db.user
        username = request.json.get('username')
        password = (request.json.get('password'))
        if not username or not password:
            return jsonify({"Message": "Missing arguements"}), 400
            # abort(400) #missing arguements
        if User.query.filter_by(username = username).first() is not None:
            return jsonify({"Message": "Username already exist"}), 400
            # abort(400) #existing user

        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        password = pwd_context.encrypt(password)
        mongo_data.insert({"username": username, "password":password})
        return jsonify({" Registered successful. username": user.username}), 201, {"Location": url_for('new_user', id = user.id, _external=True)}

    except Exception:
        abort(500)

@auth.verify_password
def verify_password(username_or_token, password):
    try:
        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.query.filter_by(username = username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        return True
    except Exception:
        abort(500)


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    try:
        token = g.user.generate_auth_token()
        return jsonify({'API_KEY': token.decode('ascii') })
    except Exception:
        abort(500)





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


@app.errorhandler(401)
def internal_error(error):
    return jsonify(
        {
            "Message": "Acess denied ! please register and login to generate API KEY"
        },
        {
            "status": 401
        }
    )



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


@app.errorhandler(500)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Bad request sent to server kindly check and resend!"
        },
        {
            "status": 500
        }
    )