import json

from models import todoDAO
from utils import decimal_encoder


def lambda_handler(event, context):

    result = todoDAO.TodoDAO().get_item(event['pathParameters']['id'])

    if result == {}:

        item = {
            'error':  "Todo not found",
            'id': event['pathParameters']['id']
        }

        return {
            "statusCode": 404,
            "body": json.dumps(item, cls=decimal_encoder.DecimalEncoder)
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(result, cls=decimal_encoder.DecimalEncoder)
        }
