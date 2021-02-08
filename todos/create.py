import json
import logging

from models import todoDAO


def lambda_handler(event, context):

    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    item = todoDAO.TodoDAO().put_item(data['text'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
