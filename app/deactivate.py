from flask import jsonify, request
from app import app, mongo
from app.audit import send_transaction


@app.route('/deactivate', methods=['PUT'])
def deactivate_card():
    global serial, serial_number, msg
    request_data = request.get_json()
    # get serial number from user and category to deactivate

    serial_no = request_data['serial_no']
    cats = request_data['category']

    # create a mongo database instance to query
    mongo_data = mongo.db.voucher
    find = mongo_data.find_one({'serial_no': serial_no})
    # finduserID = mongo_data.find_one({'userID': userID})

    # checking if serial number is valid
    if not find:
        msg =jsonify({'message': 'Invalid serial number'})
        return msg

    if cats == 1:
        serial = list(range(serial_no, serial_no + 10))
    elif cats == 2:
        serial = list(range(serial_no, serial_no + 100))
    elif cats == 3:
        serial = list(range(serial_no, serial_no + 1000))
    elif cats == 4:
        serial = list(range(serial_no, serial_no + 10000))
    elif cats == 0:
        serial = [serial_no]
    else:
        msg=jsonify({"Message": "Enter valid category"})
        return msg

    # collecting card details into voucher
    vouchers = []
    for serial_number in serial:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['activation_status'] == 1:
                # deactivate card
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 0}})

                mongo_data.find_one({'serial_no': int(serial_number)})

                vouchers.append(serial_number)
                # con = mongo_data.find({"activation_status" : 0}).count()

            elif find1['activation_status'] == 0:
                msg = "Card(s) has not been activated yet!"
                return jsonify({"Message":msg})
        else:
            break

    number = len(vouchers)
    if number > 0:
        if number == 1:
            msg = "{} cards deactivated successfully".format(number) + ' ' + 'serial number {}'.format(vouchers[0])
            send_transaction(cats, "Card deactivation", msg)
            return jsonify({"Message": msg})
        else:
            msg = "{} cards has been deactivated from range {} to {}".format(number, vouchers[0], vouchers[-1])
            send_transaction(cats, "Card Deactivation", msg)
            return jsonify({"Message": msg})
    else:
        msg = "card(s) already deactivated! to {}"
        return jsonify({"Message": msg})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"Message":"Sorry the page your are looking for is not here kindly go back" }), 404


@app.errorhandler(400)
def bad_request__error(error):
    return jsonify({"Message": "Sorry you entered wrong values kindly check and resend!"}), 400

@app.errorhandler(500)
def internal_error(error):
    mongo.session.rollback()
    return jsonify({"Message": "Sorry some errors has occured the administrator has been notified"}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"Message": "Sorry the requested method is not allowed kindly check and resend !"}),405











