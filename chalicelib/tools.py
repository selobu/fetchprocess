__all__=['today','now']
from datetime import datetime
from datetime import date

def today()->str:
    return str(date.today())
def now()-> str:
    return str(datetime.timestamp(datetime.now()))