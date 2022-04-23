import json
import os

def updateRepositoryData():
    pass

def handler(event, context):
    print('received event:')
    print(event)
  
    table_name = os.environ["STORAGE_RESPOSITORYDATA_NAME"]

    # get data from table

    # update table if data is outdated

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from your new Amplify Python lambda!')
    }