# todo-list-aws

This project contains source code and supporting files for a serverless application that you can deploy with the [Serverless Framework](https://www.serverless.com/). It includes the following files and folders.

- todos - Code for the application's Lambda function.
- tests - Static Code tests and integration for the application code. 
- serverless.yaml - A template that defines the application's AWS resources. 
- serverless.test.yaml - The integration test definition of the application. 
- package.json - App configuration that is used by serverless framework. 
- Pipfile - Dependences for the virtual environment created with pipenv.

## Configure the environment

```bash
pip3 install --user --upgrade pipenv
pipenv install
```

## Run Cyclomatic Complexity Test

```bash
pipenv run tests/complexity/test.sh
```

## Run Code Quality Test

```bash
pipenv run tests/quality/test.sh
```

## Run Security Test

```bash
pipenv run tests/security/test.sh
```

## Run Unit Test

```bash
pipenv run pytest tests/unit -v
```

## Build & Deploy the Todo app

To build and deploy your application for the first time, run the following in your shell:

```bash
sls build
sls deploy
```

## Run Integration Tests

After deploy the app:

```bash
sls test
```

## Todo API definition

### Todo list service

```bash
curl TODO_API_SERVER/todos
```

Output:
```bash
[{"text":"Deploy my first service","id":"ac90feaa11e6-9ede-afdfa051af86","checked":true,"updatedAt":1479139961304},{"text":"Learn Serverless","id":"206793aa11e6-9ede-afdfa051af86","createdAt":1479139943241,"checked":false,"updatedAt":1479139943241}]%
```

### Get a todo

```bash
# Replace the <id> part with a real id from your todos table
curl TODO_API_SERVER/todos/<id>
```

Output:
```bash
{"text":"Learn Serverless","id":"ee6490d0-aa11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":false,"updatedAt":1479138570824}%
```

### Update a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X PUT TODO_API_SERVER/todos/<id> --data '{ "text": "Learn Serverless", "checked": true }'
```

Output:
```bash
{"text":"Learn Serverless","id":"ee6490d0-aa11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":true,"updatedAt":1479138570824}%
```

### Translate a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X GET TODO_API_SERVER/todos/<id>/<language>
```

Output:
```bash
{"text":"Texto traducido automaticamente.","id":"ee6490d0-aa11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":true,"updatedAt":1479138570824}%
```

### Delete a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE TODO_API_SERVER/todos/<id>
```

No output

## Cleanup

To delete the sample application that you created, use the SLS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sls remove
```
