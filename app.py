"""_summary_

    Returns:
        _type_: _description_
"""
import requests
import subprocess
from functools import wraps
from chalice import Chalice

from chalicelib.config import Config  # type:ignore
from chalicelib import log  # type:ignore
from chalicelib import db, tools

from datetime import datetime

app = Chalice(app_name=Config.api_name)

db.initapp(app)
# ----- hack : overwriting chalice log config
log.initapp(app)
# -----

log = app.log

def catcherror(func):
    """_summary_

    Args:
        func (_type_): _description_
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """_summary_"""
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
        log.info(f"[INIT] - {name}")
        res = func(*args, **kwargs)
        log.info(f"[END] - {name}")
        return res

    return wrapper


@app.route("/")
@loginout
def index():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"hello": "world"}


@app.route("/fetch-data", methods=["GET"])
@loginout
def fetch():
    """_summary_

    Returns:
        _type_: _description_
    """
    r = requests.get(Config.externalapiurl)
    message = "unknown data"
    if r.status_code == 404:
        log.debug(f"{r.status_code} - api endpoint not found {Config.externalapiurl}")
        message = {"Error": "api endpoint not found"}
    elif r.status_code == 400:
        log.debug(f"{r.status_code} - Bad request  {Config.externalapiurl}")
        message = {"Error": "Bad request"}
    elif str(r.status_code).startswith("4"):
        message = "Error"
    if r.status_code == 200:
        error = []
        for item in r.json():
            try:
                app.db.register(item)
            except Exception as e:
                error.append(str(e))
        errors = len(error)
        errormessage = f'{errors}' + ';\n\r'.join(error)
        
        # getting timestamp

        app.db.statusreg({'timestamp': tools.now(),
                'itemsfetched': len(r.json())-errors,
                'errors': errormessage})
        
        message = {"fetch": "successfull"}

    elif str(r.status_code).startswith("2"):
        message = "success full"
    return r.status_code, message


@app.route("/view-data", methods=["GET"])
@loginout
def viewdata():
    """_summary_

    Returns:
        _type_: _description_
    """
    return app.db.registerget()


@app.route("/status", methods=["GET"])
@loginout
def status():
    """_summary_

    Returns:
        _type_: _description_
    """
    if False:
        result = subprocess.run(
            ["chalice", "logs", "--num-entries", numentries],
            check=True,
            capture_output=True,
        )
        repr(result.stdout)
    return app.db.statusget()


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
