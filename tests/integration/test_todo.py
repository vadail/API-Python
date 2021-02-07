import os
from unittest import TestCase

import boto3
import json
import pprint
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestTodo(TestCase):
    api_endpoint: str
    todo_id: str

    @classmethod
    def get_stack_name(cls) -> str:
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")
        if not stack_name:
            raise Exception(
                "Cannot find env var AWS_SAM_STACK_NAME. \n"
                "Please setup this environment variable with the stack name where we are running integration tests."
            )

        return stack_name

    def setUp(self) -> None:
        """
        Based on the provided env variable AWS_SAM_STACK_NAME,
        here we use cloudformation API to find out what the TODO URL is
        """
        stack_name = TestTodo.get_stack_name()

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}. \n" f'Please make sure stack with the name "{stack_name}" exists.'
            ) from e

        stacks = response["Stacks"]
        
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "ApiDeployment"]
        self.assertTrue(api_outputs, f"Cannot find output ApiDeployment in stack {stack_name}")
        
        self.api_endpoint = api_outputs[0]["OutputValue"]
    
    def tearDown(self):
        
        response = requests.delete(self.api_endpoint+self.todo_id)
        
    def test_CRUD_todo(self):
        """
        Call the API Gateway endpoint and check the CRUD Todo function
        """
        todoItem = {"text": "Todo description CRUD Test"}
        
        response = requests.post(self.api_endpoint, json = todoItem)
        
        self.assertEqual(response.status_code, 200)
        
        item = json.loads(response.text)
        
        self.todo_id = item["id"];
        
        response = requests.get(self.api_endpoint)
        
        self.assertEqual(response.status_code, 200)
        
        response = requests.get(self.api_endpoint+item["id"])
        
        self.assertEqual(response.status_code, 200)
        
        todoItemUpdate = {"text": "New description Update Test", "checked": "true"}
        
        response = requests.put(self.api_endpoint+item["id"], json = todoItemUpdate)
        
        self.assertEqual(response.status_code, 200)
        
        response = requests.delete(self.api_endpoint+item["id"])
        
        self.assertEqual(response.status_code, 200)
        
    def test_translate_todo(self):
        """
        Call the API Gateway endpoint and check the translate Todo function
        """
        todoItem = {"text": "Tarea a traducir"}
        
        response = requests.post(self.api_endpoint, json = todoItem)
        
        self.assertEqual(response.status_code, 200)
        
        item = json.loads(response.text)
        
        self.todo_id = item["id"];
        
        response = requests.get(self.api_endpoint+item["id"]+"/en")
        
        self.assertEqual(response.status_code, 200)
        
        item = json.loads(response.text)
        
        self.assertEqual(item["text"], "Task to translate")
