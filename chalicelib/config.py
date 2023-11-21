""" Configuration file
"""
from dataclasses import dataclass
from os import environ
appname = environ.get("APPNAME", default='fetchprocess')

@dataclass
class Config: # pylint: disable=R0902
    """Configuration app parameters
    """
    api_name: str = "future loop api"
    version: str = "0.0.1"
    api_url_prefix: str = "/api"
    api_description: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: str = ""
    items_per_user: int = 50
    api_contact= {
        "name": "Sebastian Lopez",
        "email": "sebastian.lopez@gestionhseq.com",
        "url": "https://lteam.gestionhseq.com",
        "telegram": "https://t.me/selopez",
    }
    logging_format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    app= {}
    engine = {}
    app_name: str = appname  # type:ignore
    per_page: int = 50
    externalapiurl = 'https://jsonplaceholder.typicode.com/posts'
