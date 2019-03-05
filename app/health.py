from flask import current_app as app
from flask import jsonify

from app import app


@app.route('/health')
def health():
    """\
    This function serves `/health` endpoint.
    Responses service status in json format
    that indicates server working normally.
    """

    response = dict(status='healthy',
                    container=app.config['CONTAINER_URL'],
                    project=app.config['PROJECT_URL'])

    return jsonify(response)
