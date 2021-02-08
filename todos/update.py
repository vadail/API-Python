import json
import logging

from utils import decimal_encoder
from models import todoDAO


def lambda_handler(event, context):

    data = json.loads(event['body'])

    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")

    item = todoDAO.TodoDAO().update_item(
        event['pathParameters']['id'],
        data['text'],
        data['checked'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item, cls=decimal_encoder.DecimalEncoder)
    }

    return response
