""" Configuration file
"""

from os import environ
appname = environ.get("APPNAME", default='fetchprocess')

class Config:
    """Configuration app parameters
    """
    API_NAME: str = "future loop api"
    VERSION: str = "0.0.1"
    API_URL_PREFIX: str = "/api"
    API_DESCRIPTION: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: str = ""
    items_per_user: int = 50
    API_CONTACT: object = {
        "name": "Sebastian Lopez",
        "email": "sebastian.lopez@gestionhseq.com",
        "url": "https://lteam.gestionhseq.com",
        "telegram": "https://t.me/selopez",
    }
    app: object = {}
    engine: object = {}
    APP_NAME: str = appname  # type:ignore
    PER_PAGE: int = 50
