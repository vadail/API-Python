import json

from models import todoDAO


def lambda_handler(event, context):

    # fetch all todos from the database
    result = todoDAO.TodoDAO().list_item()

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
