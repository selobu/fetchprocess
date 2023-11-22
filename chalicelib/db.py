"""
Import tables
"""
from dataclasses import dataclass
import boto3

__TableNames = ['DBDynamo','DBDynamoRatelimit','DBStatus']

def __getTables():
    dynamodb = boto3.resource("dynamodb")
    return dict((tablename, dynamodb.Table(tablename)) for tablename in __TableNames)

@dataclass
class Response:
    userId:int
    id: int
    title: str
    body: str

@dataclass
class Status:
    timestamp: str
    itemsfetched: int
    errors: str

def __register(app, data: Response):
    app.Tb['DBDynamo'].put_item(Item={
            "userId": data["userId"],
            "id": data["id"],
            "title": data["title"],
            "body": data["body"]
        })

def __statusregister(app, data:Status):
    app.Tb['DBStatus'].put_item(Item={
            "userId": data["userId"],
            "id": data["id"],
            "title": data["title"],
            "body": data["body"]
        })

def initapp(app) -> None:
    setattr(app, 'Tb', __getTables())
    register = lambda *args, **kwargs: __register(app, *args, **kwargs)
    regstatus = lambda *args, **kwargs: __statusregister(app, *args, **kwargs)
    db = {'register': register,
          'statusreg': regstatus}
    setattr(app, 'db', db)