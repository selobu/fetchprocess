"""_summary_

    Returns:
        _type_: _description_
"""

import subprocess
from chalice import Chalice
from src.config import Config

app = Chalice(app_name=Config.api_name)
Log = app.log

@app.route('/')
def index():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {'hello': 'world'}

@app.route('/fetch-data', methods=['GET'])
def fetch():
    """_summary_

    Returns:
        _type_: _description_
    """
    Log.info("Retrieving data")
    return {'fetch': 'data'}

@app.route('/view-data', methods=['GET'])
def viewdata():
    """_summary_

    Returns:
        _type_: _description_
    """
    Log.info('Viewing data')
    return {'view': 'data'}

@app.route('/status/{numentries}', methods=['GET'])
def status(numentries):
    """_summary_

    Returns:
        _type_: _description_
    """
    result = subprocess.run(['chalice', 'logs', '--num-entries', numentries],\
                             check=True, capture_output=True)
    return repr(result.stdout)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
