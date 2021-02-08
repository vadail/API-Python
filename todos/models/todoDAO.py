import boto3
import os
import uuid
import time


# TodoDAO class
class TodoDAO(object):

    # TodoDAO constructor
    def __init__(self):

        if os.environ['STAGE'] == "local":
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url="http://dynamodb:8000")

            self.table = self.get_table("TodoTable-local")

        else:
            self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            self.table = self.dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # get the table of TodoList if not this function create the table
    def get_table(self, table_name):

        table = self.dynamodb.Table(table_name)
        if "ACTIVE" in table.table_status:
            return table
        else:
            """Creates DynamoDB table"""
            print("[+] Creating Table {}...".format(table_name))

            params = {
                "TableName": table_name,
                "KeySchema": [
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    }
                ],
                "AttributeDefinitions": [
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    }
                ],
                "ProvisionedThroughput": {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }

            table = self.dynamodb.create_table(**params)

            table.meta.client.get_waiter(
                'table_exists').wait(TableName=table_name)

            return table

    def get_item(self, id):

        # fetch todo from the database
        result = self.table.get_item(
            Key={
                'id': id
            }
        )

        return result["Item"]

    def list_item(self):

        # list the todos from the database
        return self.table.scan()["Items"]

    def put_item(self, text, id=None):
        
        timestamp = str(time.time())

        item = {
            'id': str(uuid.uuid1()) if (id == None ) else id,
            'text': text,
            'checked': False,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }

        # write the todo to the database
        self.table.put_item(Item=item)

        return item

    def update_item(self, id, text, checked):

        timestamp = int(time.time() * 1000)

        # update the todo in the database
        result = self.table.update_item(
            Key={
                'id': id
            },
            ExpressionAttributeNames={
              '#todo_text': 'text',
            },
            ExpressionAttributeValues={
              ':text': text,
              ':checked': checked,
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET #todo_text = :text, '
                             'checked = :checked, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

        return result["Attributes"]

    def delete_item(self, id):

        # delete the todo from the database
        self.table.delete_item(
            Key={
                'id': id
            }
        )
