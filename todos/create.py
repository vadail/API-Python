import json
import logging

from models import todoDAO
from utils import decimal_encoder


def lambda_handler(event, context):

    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    item = todoDAO.TodoDAO().put_item(
        data['text'],
        data['id'] if ('id' in data) else None)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item, cls=decimal_encoder.DecimalEncoder)
    }

    return response
