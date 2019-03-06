import boto3


def get_dynamo(key: str, secret: str, region: str, endpoint=None):
    """
    Setups connection to DynamoDB.
    :return: Dynamo and Table object.
    """

    # setup aws session
    boto3.setup_default_session(aws_access_key_id=key,
                                aws_secret_access_key=secret,
                                region_name=region)

    # setup dynamodb connection
    dynamo = boto3.resource('dynamodb', endpoint_url=endpoint)
    table = dynamo.Table('devops-challenge')

    # checking connection
    is_table_existing = table.table_status in ("CREATING", "UPDATING", "DELETING", "ACTIVE")

    return dynamo, table
