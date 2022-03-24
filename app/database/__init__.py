import boto3
from botocore.exceptions import ClientError
from app.config import settings
from boto3.dynamodb import table
class Dynamo:
    _instances = {}

    def create_reso(self):
        try:
            if "resource" not in self._instances:
                dynamodb = \
                    boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=settings.verify,
                                   region_name=settings.region_name,
                                   aws_access_key_id=settings.aws_access_key_id,
                                   aws_secret_access_key = settings.aws_secret_access_key)
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise e

    def create_table(self,dynamodb=None):
        try:
            if not dynamodb or "resource" not in self._instances:
                dynamodb = \
                    boto3.resource('dynamodb',
                                   endpoint_url=settings.endpoint_url,
                                   verify=settings.verify,
                                   region_name=settings.region_name,
                                   aws_access_key_id=settings.aws_access_key_id,
                                   aws_secret_access_key=settings.aws_secret_access_key)
                self._instances["resource"] = dynamodb
            return self._instances["resource"]
        except ClientError as e:
            raise "Error"

    def create_users_table(dynamodb=None):
        dynamodb = \
            boto3.resource('dynamodb',
                           endpoint_url=settings.endpoint_url,
                           verify=settings.verify,
                           region_name=settings.region_name,
                           aws_access_key_id=settings.aws_access_key_id,
                           aws_secret_access_key=settings.aws_secret_access_key)
        # Table defination
        table = dynamodb.create_table(
            TableName='table',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    # AttributeType defines the data type. 'S' is string type and 'N' is number type
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                # ReadCapacityUnits set to 10 strongly consistent reads per second
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
            }
        )
        return table

    def get_table(self,dynamodb=None):
        if "table" not in self._instances:
            dynamodb = self.create_reso()
            table = dynamodb.Table(settings.table)
            self._instances["table"] = table
        return self._instances["table"]

dynamo = Dynamo()