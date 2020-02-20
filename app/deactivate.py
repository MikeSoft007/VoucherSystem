from flask import jsonify, request
from app import app, mongo


@app.route('/deactivate', methods=['PUT'])
def deactivate_card():
    global ser, serial_number
    request_data = request.get_json()
    # get serial number from user and category to deactivate
    serial_no = request_data['serial_no']
    category = request_data['category']

    # create a mongo database instance to query
    mongo_data = mongo.db.pins
    find = mongo_data.find_one({'serial_no': serial_no})

    # checking if serial number is valid
    if not find:
        return jsonify({'message': 'Invalid serial number'})


    if category == 1:
        ser = list(range(serial_no, serial_no + 10))
    elif category == 2:
        ser = list(range(serial_no, serial_no + 100))
    elif category == 3:
        ser = list(range(serial_no, serial_no + 1000))
    elif category == 4:
        ser = list(range(serial_no, serial_no + 10000))
    elif category == 0:
        ser = [serial_no]
    else:
        return jsonify({"Message": "Enter valid category"})

    # collecting card details into voucher
    vouchers = []
    for serial_number in ser:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['activation_status'] == 1:
                # deactivate card
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 0}})

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
                    "Message": "{} cards deactivated successfully".format(number) + ' ' + 'serial number {}'.format(vouchers[0]),
                }
            )
        else:
            return jsonify(
                {
                    "Card Range": "{} cards has been deactivated from range {} to {}".format(number, vouchers[0], vouchers[-1])
                }
            )
    else:
        return jsonify({"Message": "cards already deactivated!"})
