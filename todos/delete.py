from models import todoDAO


def lambda_handler(event, context):

    # delete todo
    todoDAO.TodoDAO().delete_item(event['pathParameters']['id'])

    # create a response
    response = {
        "statusCode": 200
    }

    return response
