from flask import jsonify, request, abort
from app import app, mongo, cur_time_and_date
from app import auth

@app.route('/activate', methods=['PUT'])
@auth.login_required
def activate_card():
    global serial, serial_number, msg
    request_data = request.get_json()
    mongo_data = mongo.db.voucher
    logs = mongo.db.act_logs

    # get serial number from user and category to activate
    dealer_id = request_data['dealer_id']
    serial_no = int(request_data['serial_no'])
    cat = request_data['category']
    batch = request_data['batch']

    # create a mongo database instance to query

    find = mongo_data.find_one({'serial_no': serial_no})
    findbatch = mongo_data.find_one({'batch': batch})
    finddealer = mongo_data.find_one({'dealer_id': dealer_id})


    # checking if serial number and userID is valid
    if not finddealer:
        return jsonify({'message': 'Invalid dealer ID'})

    if not find:
        return jsonify({'message': 'Invalid serial number'})

    if not findbatch:
        return jsonify({'message': 'Invalid batch number'})



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
        msg =jsonify({"Message": "Enter valid category 0 for single card 1=10 cards, 2 = 100 cards, 3 = 1000 cards, 4 = 10000 cards"})
        return msg


    # collecting card details into voucher
    vouchers = []
    for serial_number in serial:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number), 'batch': int(batch)})
        if find1:
            if find1['dealer_id'] !='None':
                if find1['activation_status'] == 0:
                    # activate card
                    mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 1}})

                    mongo_data.find_one({'serial_no': int(serial_number)})
                    logs.insert(
                        {
                            "daelerID": dealer_id,
                            "serial_number": serial_number,
                            "batch": batch,
                            "status": "Activatted",
                            "to": dealer_ids,
                            "date": cur_time_and_date()
                        }
                    )
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
             return jsonify({"Message": msg})
        else:
            msg = "{} cards has been activated from range {} to {}".format(number, vouchers[0], vouchers[-1])
            return jsonify({"Message": msg})
    else:
        msg ="card(s) already activated! to Merchant with {}".format(dealer_ids)
        return jsonify({'Message': msg})


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