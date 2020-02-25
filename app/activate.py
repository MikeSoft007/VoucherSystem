from flask import jsonify, request
from app import app, mongo


@app.route('/activate', methods=['PUT'])
def activate_card():
    global serial, serial_number
    request_data = request.get_json()
    # get serial number from user and category to activate
    serial_no = request_data['serial_no']
    cat = request_data['category']

    # create a mongo database instance to query
    mongo_data = mongo.db.voucher
    find = mongo_data.find_one({'serial_no': serial_no})

    # checking if serial number is valid
    if not find:
        return jsonify({'message': 'Invalid serial number'})


    if cat == 1:
        serial = list(range(serial_no, serial_no + 10))
    elif cat == 2:
        serial = list(range(serial_no, serial_no + 100))
    elif cat == 3:
        serial = list(range(serial_no, serial_no + 1000))
    elif cat == 4:
        serial = list(range(serial_no, serial_no + 10000))
    elif cat == 0:
        serial = [serial_no]
    else:
        return jsonify({"Message": "Enter valid category"})

    # collecting card details into voucher
    vouchers = []
    for serial_number in serial:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['activation_status'] == 0 and find1['dealer_id'] is not None:
                # activate card
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 1}})

                mongo_data.find_one({'serial_no': int(serial_number)})

                vouchers.append(serial_number)
                # con = mongo_data.find({"activation_status" : 0}).count()
        else:
            break

    number = len(vouchers)
    if number > 0:
        if number == 1:
            return jsonify(
                {
                    "Message": "{} card activated successfully".format(number) + ' ' + 'serial number {}'.format(vouchers[0]),
                }
            )
        else:
            return jsonify(
                {
                    "Message": "{} cards has been activated from range {} to {}".format(number, vouchers[0], vouchers[-1])
                }
            )
    else:
        return jsonify({"Message": "card(s) already activated! or not yet assigned"})
