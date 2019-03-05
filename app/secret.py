from flask import g
from flask import abort
from flask import jsonify

from app import app


@app.route('/secret')
def secret():
    """\
    This function serves `/secret` endpoint.
    Gets secret code from database then then renders json in response.

    When code not found returns HTTP 500 error.
    """

    try:
        # requesting data from dynamodb
        response = g.table.get_item(
            Key={
                'code_name': app.config['CODENAME'],
            }
        )

        # extracting secret_code
        secret_code = response['Item']['secret_code']

        # send response
        return jsonify(dict(secret_code=secret_code))
    except KeyError:
        # secret_code was not found, show HTTP 500 error
        abort(500, 'secret_code was not found in database')
