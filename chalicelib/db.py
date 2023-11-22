"""
Import tables
"""
from dataclasses import dataclass
from chalicelib import tools
import boto3
from json import loads
from pathlib import Path
from boto3.dynamodb.conditions import Key
from json import dumps
from os import environ

__TableNames = ['Demo','RateLimit','Status']

client = boto3.client('dynamodb')# catch resource in exception

if (DEBUG:=environ.get("DEBUG", default=True)) == True:
    dynamodb = boto3.resource("dynamodb", endpoint_url='http://localhost:8002')
else:
    dynamodb = boto3.resource("dynamodb")

def  __createlocaltables(dynamodb):
    # reading json data
    curr_path = Path(__file__).parent
    with open(curr_path.joinpath('../pipeline.json'),'r') as fopen:
        res = loads(fopen.read())
    tables = []
    for key,value in res['Resources'].items():
        if value['Type'] != "AWS::DynamoDB::Table":
            continue
        tables.append(value['Properties'])
    for table in tables:
        # cheking if table exists
        try:
            dynamodb.create_table(
                TableName=table['TableName'],
                AttributeDefinitions=table['AttributeDefinitions'],
                BillingMode=table['BillingMode'],
                # ContributorInsightsSpecification=table['ContributorInsightsSpecification'],
                DeletionProtectionEnabled=table['DeletionProtectionEnabled'],
                KeySchema=table['KeySchema'],
                TableClass=table['TableClass'],
                Tags=table['Tags']
                )
            print(f"successfully created table: {table['TableName']}")
        except client.exceptions.ResourceInUseException as e:
            print(f"cannot create table: {table['TableName']}  error: {e}")
            ...

def __getTables():
    if DEBUG:
         __createlocaltables(dynamodb)
    return  dict((tablename, dynamodb.Table(tablename)) for tablename in __TableNames)

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

class Db:
    ...

def __register(app, data: Response):
    app.Tb['Demo'].put_item(Item={
            "timestamp": tools.now(),
            "userId": data["userId"],
            "id": data["id"],
            "title": data["title"],
            "body": data["body"]
        })

def __registerget(app, keys:list=["userId", "timestamp"], LastEvaluatedKey:dict=None)-> dict:
    if LastEvaluatedKey is not None:
        return app.Tb['Demo'].scan(Limit=10, LastEvaluatedKey=LastEvaluatedKey)
    return app.Tb['Demo'].scan(Limit=10)

def __statusregister(app, data:Status):
    app.Tb['Status'].put_item(Item={
            "date": tools.today(),
            "timestamp": data["timestamp"],
            "itemsfetched": data["itemsfetched"],
            "errors": data["errors"],
        })
    
def __statusget(app):
    table = app.Tb['Status']
    print('reading info')
    res = table.query(
        KeyConditionExpression=Key('date').eq(tools.today()),
        Limit=1,
        ScanIndexForward=False)
    return res

def initapp(app) -> None:
    setattr(app, 'Tb', __getTables())
    register = lambda *args, **kwargs: __register(app, *args, **kwargs)
    statusreg = lambda *args, **kwargs: __statusregister(app, *args, **kwargs)
    statusget = lambda *args, **kwargs: __statusget(app, *args, **kwargs)
    registerget = lambda *args, **kwargs: __registerget(app, *args, **kwargs)
    setattr(Db,'register', register)
    setattr(Db,'statusreg', statusreg)
    setattr(Db,'statusget', statusget)
    setattr(Db,'registerget', registerget)
    setattr(app, 'db', Db)
