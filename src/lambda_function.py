import json
import sys
from revenue import SearchEngineRevenue

def lambda_handler(event, context):
    # TODO implement
    logfile = 'data.tsv'
    sengine = SearchEngineRevenue(logfile)
    sengine.get_revenue()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }