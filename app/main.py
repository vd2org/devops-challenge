from flask import g

from app import app
import os

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

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
    dynamo = boto3.resource('dynamodb', endpoint_url=os.environ.get('DYNAMO_ENDPOINT'))
    table = dynamo.Table('devops-challenge')

    # checking connection
    is_table_existing = table.table_status in ("CREATING", "UPDATING", "DELETING", "ACTIVE")

except KeyError as e:
    # missing configuration environment
    raise RuntimeError('Unable to get configuration env var `%s`' % str(e)) from e

except EndpointConnectionError as e:
    # connection error
    raise RuntimeError('Dynamo is db not available.') from e

except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        # required table not found in dynamodb
        raise RuntimeError('Required table does not exist.') from e
    if e.response['Error']['Code'] in ('UnrecognizedClientException', 'AccessDeniedException'):
        # required table not found in dynamodb
        raise RuntimeError('Dynamo error. Probably your access token is invalid.') from e
    # reraise other exceptions
    raise


@app.before_request
def before_request():
    """\
    Setups database variables in application context.
    """
    g.dynamo = dynamo
    g.table = table


if __name__ == '__main__':
    app.run(debug=True)
