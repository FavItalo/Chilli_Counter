import boto3
import json

def get_all_dynamodb_items(table_name):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    items = []
    response = table.scan()
    items.extend(response.get('Items', []))

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))
    return items

def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'data': get_all_dynamodb_items('chilli_count_hist')
    }
