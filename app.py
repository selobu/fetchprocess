"""_summary_

    Returns:
        _type_: _description_
"""
import requests
import subprocess
from functools import wraps
from chalice import Chalice

from chalicelib.config import Config # type:ignore
from chalicelib.log import configlogging # type:ignore

app = Chalice(app_name=Config.api_name)

# -----
# hack : overwriting chalice log config
configlogging(app)
# -----

log = app.log

def catcherror(func):
    """_summary_

    Args:
        func (_type_): _description_
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """_summary_
        """
        res = func(*args, **kwargs)
        return res
    
    return wrapper

def loginout(func):
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
        name = func.__qualname__
        log.info(f'[INIT] - {name}')
        res = func(*args, **kwargs)
        log.info(f'[END] - {name}')
        return res

    return wrapper

@app.route('/')
@loginout
def index():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {'hello': 'world'}

@app.route('/fetch-data', methods=['GET'])
@loginout
def fetch():
    """_summary_

    Returns:
        _type_: _description_
    """
    r = requests.get(Config.externalapiurl)
    message = "unknown data"
    if r.status_code == 404:
        log.debug(f'{r.status_code} - api endpoint not found {Config.externalapiurl}')
        message =  {"Error": 'api endpoint not found'}
    elif r.status_code == 400:
        log.debug(f'{r.status_code} - Bad request  {Config.externalapiurl}')
        message = {"Error": 'Bad request'}
    elif str(r.status_code).startswith('4'):
         message = "Error"
    if r.status_code == 200:
        data = r.json()
        
        message = {'fetch': 'data'}
    elif str(r.status_code).startswith('2'):
        message = 'success full'
    log.info(r.status_code)
    return r.status_code, message

@app.route('/view-data', methods=['GET'])
@loginout
def viewdata():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {'view': 'data'}

@app.route('/status/{numentries}', methods=['GET'])
@loginout
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
