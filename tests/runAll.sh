pip install awscli
pip3 install awscli

echo -e "\nBorrando posible grupo de log:"
aws logs delete-log-group --log-group-name /aws/api-gateway/serverless-rest-api-with-dynamodb-efimero

echo -e "\nSalida:"
echo $?

exit 1