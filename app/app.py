"""_summary_

    Returns:
        _type_: _description_
"""

import subprocess
from functools import wraps
from chalice import Chalice

# add src to the syspath
from sys import path as syspath 
from pathlib import Path
from os.path import abspath

def icludepath():
    print('Cekcing configuration')
    print(__file__)
    cp = Path(__file__).parent
    print(cp)
    if abspath(cp) not in syspath:
        print('CP added')
        syspath.append(abspath(cp))
    else:
        print('Not added')
    print('====')
icludepath()
# ---
try:
    from app.src.config import Config # type:ignore
    from app.src.log import configlogging # type:ignore
except ImportError:
    from .src.config import Config # type:ignore
    from .src.log import configlogging # type:ignore

app = Chalice(app_name=Config.api_name)

# -----
# hack : overwriting chalice log config
configlogging(app)
# -----
log = app.log

def docs(func):
    """automatically rest api document generation

    Args:
        func (_type_): _description_

    Returns:
        _type_: _description_
    """
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
