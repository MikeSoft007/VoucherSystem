from app import app, db, mongo
from flask import jsonify



@app.route('/', methods=['GET'])
def index():
    msg = "Welcome!, with this API you can activate or deactivate cards specifying the serial number and category (range) of the card(s) N.B: only assigned cards can be activated!!!, and only activated cards can be deactivated  <<HAPPY TESTING>>!"
    return jsonify({"Message": msg})



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