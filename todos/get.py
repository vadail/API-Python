import json

from models import todoDAO


def lambda_handler(event, context):

    result = todoDAO.TodoDAO().get_item(event['pathParameters']['id'])

    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
