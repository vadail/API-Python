import json

from models import todoDAO
from utils import decimal_encoder


def lambda_handler(event, context):

    result = todoDAO.TodoDAO().get_item(event['pathParameters']['id'])
    
    print("Imprimo el elemento")
    print(result)
    
    if result == {}:
        
        item = {
            'error':  "Todo not found",
            'id': event['pathParameters']['id']
        }

        print("404")
        return {
            "statusCode": 404,
            "body": json.dumps(item, cls=decimal_encoder.DecimalEncoder)
        }
    else:
        print("200")
        return {
            "statusCode": 200,
            "body": json.dumps(result, cls=decimal_encoder.DecimalEncoder)
        }
