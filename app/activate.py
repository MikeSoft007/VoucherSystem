from flask import jsonify, request
from app import app, mongo
from app.audit import send_transaction



@app.route('/activate', methods=['PUT'])
def activate_card():
    global serial, serial_number, msg
    request_data = request.get_json()
    mongo_data = mongo.db.voucher

    # get serial number from user and category to activate

    serial_no = request_data['serial_no']
    cat = request_data['category']

    # create a mongo database instance to query

    find = mongo_data.find_one({'serial_no': serial_no})


    # checking if serial number and userID is valid
    if not find:
        return jsonify({'message': 'Invalid serial number'})

    dealer_ids = mongo_data.find_one(
        {"serial_no":serial_no},
        {"dealer_id":1, "_id":0}
    )


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
        msg =jsonify({"Message": "Enter valid category"})
        return msg


    # collecting card details into voucher
    vouchers = []
    for serial_number in serial:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['activation_status'] == 0 and find1['dealer_id'] !='None':
                # activate card
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 1}})

                mongo_data.find_one({'serial_no': int(serial_number)})

                vouchers.append(serial_number)
                # con = mongo_data.find({"activation_status" : 0}).count()

            elif find1['dealer_id'] =='None':
                 msg = jsonify({"Message":"Card(s) has not been assigned yet!"})
                 return msg
        else:
            break

    number = len(vouchers)
    if number > 0:
        if number == 1:
             msg =  "{} card activated successfully".format(number) + ' ' + 'serial number {}'.format(vouchers[0])
             send_transaction(cat,"Card activation", msg)
             return jsonify({"Message": msg})
        else:
            msg = "{} cards has been activated from range {} to {}".format(number, vouchers[0], vouchers[-1])
            send_transaction(cat, "Card Activation", msg)
            return jsonify({"Message": msg})
    else:
        msg ="card(s) already activated! to Merchant with {}".format(dealer_ids)
        return jsonify({'Message': msg})