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
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.create_table(
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
                            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}])
                    
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
        self.dynamodb = None

    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_list_item(self):
    
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.create_table(
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
                            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}])
                    
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
        items = todoDB.list_item()
        
        assert 1 == len(items)
        
        table.delete()
        self.dynamodb = None

    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_put_item(self):
    
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.create_table(
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
                            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}])
              
        data = {'text': "Test Todo"}
        
        todoDB = todos.models.todoDAO.TodoDAO()
        item = todoDB.put_item(data["text"])
        
        response = table.get_item(Key={'id':item['id']})
        actual_output = response['Item']
        assert actual_output == item
        
        table.delete()
        self.dynamodb = None
    
    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_update_item(self):
    
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.create_table(
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
                            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}])
                    
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
        item = todoDB.update_item(data["id"],"Texto modificado",True)
        
        assert item["text"] == "Texto modificado"
        assert item["checked"] == True
        
        table.delete()
        self.dynamodb = None

    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_delete_item(self):
    
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.create_table(
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
                            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}])
                    
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
        todoDB.delete_item(data["id"])
        
        response = table.get_item(Key={'id':data['id']})
        
        with self.assertRaises(KeyError) as raises:
            item = response["Item"]
        
        table.delete()
        self.dynamodb = None

    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_get_table(self):
    
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = os.environ['DYNAMODB_TABLE']
        table = dynamodb.create_table(
                            TableName=table_name,
                            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
                            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}])
                    
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
        response = todoDB.get_table(table_name)
        
        assert response == table
        
        table.delete()
        self.dynamodb = None

    @mock.patch.dict(os.environ, {"DYNAMODB_TABLE": "TodoTable-mock", "STAGE": "mock"})
    @mock_dynamodb2    
    def test_get_table_not_active(self):
    
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = os.environ['DYNAMODB_TABLE']
        
        todoDB = todos.models.todoDAO.TodoDAO()
        
        with self.assertRaises(ClientError):
            response = todoDB.get_table(table_name)
            
        self.dynamodb = None
