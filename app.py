"""_summary_

    Returns:
        _type_: _description_
"""

import subprocess
from chalice import Chalice
from src.config import Config
from src.log import configlogging
from functools import wraps
app = Chalice(app_name=Config.api_name)

# -----
# hack : overwriting chalice log config
configlogging(app)
# ----- 
log = app.log

def docs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """_summary_

        Returns:
            _type_: _description_
        """
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    """_summary_

    Returns:
        _type_: _description_
    """
    log.info('information')
    return {'hello': 'world'}

@app.route('/fetch-data', methods=['GET'])
def fetch():
    """_summary_

    Returns:
        _type_: _description_
    """
    log.info("Retrieving data")
    return {'fetch': 'data'}

@app.route('/view-data', methods=['GET'])
def viewdata():
    """_summary_

    Returns:
        _type_: _description_
    """
    log.info('Viewing data')
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
