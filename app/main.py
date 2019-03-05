from flask import g

from app import app
import os

import boto3
from botocore.exceptions import ClientError

import health
import secret

try:
    # loading configuration environment
    app.config.from_mapping(CODENAME=os.environ['CODENAME'],
                            CONTAINER_URL=os.environ['CONTAINER_URL'],
                            PROJECT_URL=os.environ['PROJECT_URL'])

    # setup aws session
    boto3.setup_default_session(aws_access_key_id=os.environ['AWS_KEY'],
                                aws_secret_access_key=os.environ['AWS_SECRET'],
                                region_name=os.environ['AWS_REGION'])

    # setup dynamodb connection
    # dynamodb_client = boto3.client('dynamodb', endpoint_url=os.environ.get('DYNAMO_ENDPOINT'))
    g.dynamo = boto3.resource('dynamodb', endpoint_url=os.environ.get('DYNAMO_ENDPOINT'))
    g.table = g.dynamo.Table('devops-challeng')

except KeyError as e:
    # missing configuration environment
    raise RuntimeError('Unable to get configuration env var `%s`' % str(e)) from e
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        # required table not found in dynamodb
        raise RuntimeError('Required table does not exist.') from e
    if e.response['Error']['Code'] == 'EndpointConnectionError':
        # connection error
        raise RuntimeError('Dynamo db not avaliable.') from e

    # reraise other exceptions
    raise

if __name__ == '__main__':
    app.run(debug=True)
