import requests as reqs


def send_transaction(userID, action_type, action_description):

    data = {
        'userID': userID,
        'action_type': action_type,
        'action_description': action_description
    }

    response = reqs.post('https://instant-transaction.herokuapp.com/audit_trail', json=data)

    print(response.status_code)
    print(response.json())

    return response.json()


