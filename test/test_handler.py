from moto import mock_s3
import pandas as pd
from src import lambda_function
import boto3
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from src import revenue


test_s3_event = {
    "Records": [{
        "s3": {
            'bucket': {'name': 'search-engine-revenue-input'},
            'object': {
                'key': 's3://search-engine-revenue-input/data.tsv'
            }
        }
    }]}


def test_capital_case():
    assert 'Semaphore' == 'Semaphore'



def test_create_bucket(s3):
    # s3 is a fixture defined above that yields a boto3 s3 client.
    # Feel free to instantiate another boto3 S3 client -- Keep note of the region though.
    s3.create_bucket(Bucket="somebucket")

    result = s3.list_buckets()
    assert len(result['Buckets']) == 1
    assert result['Buckets'][0]['Name'] == 'somebucket'






    
