import unittest
import boto3
import uuid
import time
import os
import mock
from moto import mock_dynamodb2
from botocore.exceptions import ClientError

import todos.models.todoDAO

class TestTodoDAOFunctions(unittest.TestCase):
        
    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_get_item(self):

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        table = dynamodb.create_table(
            TableName=os.environ['DYNAMODB_TABLE'],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=os.environ['DYNAMODB_TABLE'])
        if (table.table_status != 'ACTIVE'):
            raise AssertionError()
    
        timestamp = str(time.time())
        
        data = {
                'id': str(uuid.uuid1()),
                'text': "Test Todo",
                'checked': False,
                'createdAt': timestamp,
                'updatedAt': timestamp,
            }
        
        table.put_item(Item=data)
        
        todoDB = todos.models.todoDAO.TodoDAO()
        item = todoDB.get_item(data["id"])
        
        assert data == item
        
        table.delete()
        dynamodb = None
