import json

from models import todoDAO
from utils import decimal_encoder


def lambda_handler(event, context):

    # fetch all todos from the database
    result = todoDAO.TodoDAO().list_item()

    return {
        "statusCode": 200,
        "body": json.dumps(result, cls=decimal_encoder.DecimalEncoder)
    }
