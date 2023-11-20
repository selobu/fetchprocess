#coding: utf-8
"""hack to configure the logging
"""
import logging
from chalicelib.config import Config

def configlogging(app=None)-> logging.Logger:
    """_summary_

    Args:
        app (_type_, optional): valid chalice app

    Returns:
        logging.Logger: return the logger
    """
    app.debug=True # equivalent to .setLevel(logging.DEBUG)
    log = app.log
    handler = log.handlers[0]
    formatter = logging.Formatter(Config.logging_format)
    handler.setFormatter(formatter)
    return log
