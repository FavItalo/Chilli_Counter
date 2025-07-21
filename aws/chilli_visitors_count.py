import requests as rq
import pandas as pd
import boto3 as bt

def access_chilli(time:int):
    
    url_contador = "https://hotelchilli.com.br/api/get-guest-count"
    
    try:
        result = rq.get(url_contador)
        
        if result.status_code == 200:
            counter_element = int(result.content)

            return {"date": time, "visitors": counter_element}
    
    except Exception as e:
        raise f"Failed to access counter: {e}"

def lambda_handler(event, context):
    time = int(pd.to_datetime("now").timestamp())    
    returned_events = access_chilli(time)
    
    try:
        dynamo_db = bt.resource("dynamodb")
        table = dynamo_db.Table("chilli_count_hist")
    except Exception as e:
        raise f"Failed to load dynamo: {e}"
    
    try:
        table.put_item(Item=returned_events)
        return "Success"
    except Exception as e:
        raise f"Failed to insert item: {e}"