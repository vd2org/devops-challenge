from flask import g

from app import app
import os

from botocore.exceptions import ClientError, EndpointConnectionError

import dynamo
import health
import secret

try:
    # loading configuration environment
    app.config.from_mapping(CODENAME=os.environ['CODENAME'],
                            CONTAINER_URL=os.environ['CONTAINER_URL'],
                            PROJECT_URL=os.environ['PROJECT_URL'])

    dynamo, table = dynamo.get_dynamo(os.environ['AWS_KEY'], os.environ['AWS_SECRET'],
                                      os.environ['AWS_REGION'], os.environ.get('DYNAMO_ENDPOINT'))

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
