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
    def test_get_table_not_active(self):
    
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ['DYNAMODB_TABLE']
        
        todoDB = todos.models.todoDAO.TodoDAO()
        
        with self.assertRaises(ClientError):
            response = todoDB.get_table(table_name)
            
        self.dynamodb = None
