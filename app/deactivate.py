from flask import jsonify, request
from app import app, mongo


@app.route('/deactivate', methods=['PUT'])
def deactivate_card():
    global serial, serial_number
    request_data = request.get_json()
    # get serial number from user and category to deactivate
    serial_no = request_data['serial_no']
    cats = request_data['category']

    # create a mongo database instance to query
    mongo_data = mongo.db.voucher
    find = mongo_data.find_one({'serial_no': serial_no})

    # checking if serial number is valid
    if not find:
        return jsonify({'message': 'Invalid serial number'})


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
        return jsonify({"Message": "Enter valid category"})

    # collecting card details into voucher
    vouchers = []
    for serial_number in serial:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['activation_status'] == 1 and find1['dealer_id'] is not None:
                # deactivate card
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 0}})

                mongo_data.find_one({'serial_no': int(serial_number)})

                vouchers.append(serial_number)
                # con = mongo_data.find({"activation_status" : 0}).count()

            elif find1['dealer_id'] is None:
                return jsonify({"Message": "Card(s) has not been assigned yet!"})
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
        return jsonify({"Message": "card(s) already deactivated!"})













