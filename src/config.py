__all__= ['Config']

from os import environ
appname = environ.get("APPNAME", default='fetchprocess')

class Config(object):
    API_NAME: str = "QRSchool api"
    VERSION: str = "0.0.2"
    API_URL_PREFIX: str = "/api"
    API_DESCRIPTION: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: str = ""
    items_per_user: int = 50
    API_CONTACT: object = {
        "name": "lteam",
        "email": "sebastian.lopez@gestionhseq.com",
        "url": "https://lteam.gestionhseq.com",
        "telegram": "https://t.me/selopez",
    }
    JWT_SECRET_KEY: str = jwt_key
    WTF_CSRF_SECRET_KEY: str = jwt_key * 2
    app: object = {}
    engine: object = {}
    ECHO: bool = echo_value  # type:ignore
    APP_NAME: str = appname  # type:ignore
    FLASK_ADMIN_SWATCH: str = "cerulean"  # admin bootswatch theme
    ADMIN_TEMPLATE_NAME: str = "bootstrap4"
    TESTING: bool = False
    PER_PAGE: int = 50