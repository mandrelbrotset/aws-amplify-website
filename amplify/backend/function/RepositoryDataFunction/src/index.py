import json
import os
import boto3
import urllib.request
import urllib.error
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
# maximum cache age in hours
max_cache_age = 12.0

def update_repository_data_table(repo_data):
    table_name = os.environ["STORAGE_REPOSITORY_NAME"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        with table.batch_writer() as batch:
            date_updated = datetime.utcnow()

            for repository in repo_data:
                item = {
                    'Id'            : str(repository['id']),
                    'Name'          : repository['name'],
                    'Description'   : repository['description'],
                    'Language'      : repository['language'],
                    'Stars'         : str(repository['stargazers_count']),
                    'Url'           : repository['url'],
                    'CreatedAt'     : repository['created_at'],
                    'UpdatedAt'     : date_updated.strftime(time_format)
                }
                batch.put_item(Item=item)

        logger.info("Successfully updated table!")
        return True
    except Exception as e:
        logger.error(e)
        return False


def update_repository_data():
    github_api_url = os.environ["GITHUB_API_URL"]

    try:
        with urllib.request.urlopen(github_api_url, timeout=2) as response:
            logger.info("Received HTTP {} response while making get request to {}".format(response.status, github_api_url))
            
            github_data = json.loads(response.read().decode())
            status = update_repository_data_table(github_data)

            if status:
                logger.info("Updated cache")
                return True
            return False

    except urllib.error.HTTPError as e:
        logger.info("Received HTTP {} : {} making get request to {}".format(e.code, e.reason, github_api_url))
        return False


def get_respository_data():
    table_name = os.environ["STORAGE_REPOSITORY_NAME"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.scan(Limit=1)
        repo_data = response['Items'][0]

        current_time = datetime.utcnow()
        last_updated_time = datetime.strptime(repo_data['UpdatedAt'], time_format)
        time_difference = current_time - last_updated_time

        if time_difference.seconds / 3600 > max_cache_age:
            update_repository_data()

        response = table.scan()
        logger.info("Retrieved {} items from cache".format(len(response['Items'])))
        return response['Items']

    except Exception as e:
        logger.error("Received HTTP {} : {} while querying cache".format(e.response['ResponseMetadata']['HTTPStatusCode'], e.response['Error']['Message']))
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
        'body': json.dumps(repository_data)
    } 