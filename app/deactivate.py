from flask import jsonify, request
from app import app, mongo


@app.route('/deactivate', methods=['PUT'])
def deactivate():
    request_data = request.get_json()

    # requesting serial number
    serial_number = request_data['serial_no']
    category = request_data['category']

    if category == 1:
        msg = 'brick'
    elif category == 2:
        msg = 'batch'
    elif category == 3:
        msg = 'case'
    elif category == 4:
        msg = 'pack'
    else:
        msg = 'one card'

    # check if serial number is valid and exists in the database
    mongo_data = mongo.db.pins
    find = mongo_data.find_one({'serial_no': serial_number})

    if not find:
        return jsonify({'message': 'Invalid serial number'})


    mongo_data.update_one({'serial_no': serial_number}, {"$set": {"activation_status": 0}})

    find1 = mongo_data.find_one({'serial_no': serial_number})
    return jsonify({'serial_no': find1['serial_no'], 'activation_status': find1['activation_status'], 'category': msg})