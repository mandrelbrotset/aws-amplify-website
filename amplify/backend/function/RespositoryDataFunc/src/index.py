import json
import os
import boto3
import urllib.request
import urllib.error
from datetime import datetime

time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
# maximum cache age in hours
max_cache_age = 12.0

def update_repository_data_table(repo_data):
    table_name = os.environ["STORAGE_RESPOSITORYDATA_NAME"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        with table.batch_writer() as batch:
            date_updated = datetime.utcnow()

            for repository in repo_data:
                item = {
                    'Id'            : repository['id'],
                    'Name'          : repository['name'],
                    'Description'   : repository['description'],
                    'Language'      : repository['language'],
                    'Stars'         : repository['stargazers_count'],
                    'Url'           : repository['url'],
                    'CreatedAt'     : repository['created_at'],
                    'UpdatedAt'     : date_updated.strftime(time_format)
                }
                batch.put_item(Item=item)

        # log success
        # 

        return True
    except Exception as e:
        print(e)
        # log error
        #

        return False


def update_repository_data():
    github_api_url = os.environ["GITHUB_API_URL"]

    try:
        with urllib.request.urlopen(github_api_url, timeout=2) as response:
            # log success
            #{"status"  : response.status,
            # "message" : "success"}

            github_data = json.loads(response.read().decode())
            status = update_repository_data_table(github_data)

            if status:            
                return True

            return False

    except urllib.error.HTTPError as e:
        print(e)
        
        # log error
        #{"status"  : e.code,
        # "message" : e.reason}
        return False


def get_respository_data():
    table_name = "RespositoryData-dev"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.scan(Limit=1)
        repo_data = response['Items'][0]

        current_time = datetime.utcnow()
        last_updated_time = datetime.strptime(repo_data['UpdatedAt'], time_format)
        time_difference = current_time - last_updated_time

        if time_difference.seconds / 3600 > max_cache_age:
            # log info about update
            update_repository_data()

        response = table.scan()

        # log success
        #{"status"  : response['ResponseMetadata']['HTTPStatusCode'], 
        # "message" : "received " + len(response['Items']) + " items"}

        return response['Items']

    except Exception as e:
        print(e)

        # log error
        #{"status"  : e.response['ResponseMetadata']['HTTPStatusCode'],
        # "message" : e.response['Error']['Message']}
        return None


def handler(event, context):
    repository_data = get_respository_data()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': repository_data
    } 