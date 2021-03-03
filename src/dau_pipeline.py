import sys
import json
import pandas as pd
import boto3
import tqdm

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

def source_json_data(xia_bucket, path_to_json):
    """ Loading JSON data from S3

    The objective of the function is to load JSON data from an AWS S3 bucket
    into memory. The intention is this script could run on an EC2 or Lambda instance
    to load data from XIA agents.

    Limitations: The current script is built specifically for the DAU metadata.
    This code will be updated based on requirements from additional metadata
    sources, such as edX.

    Args:
        xia_bucket (str): Name of the S3 bucket.
        path_to_json (str): Path to the file starting at the S3 bucket root
        directory (e.g., s3://[xia_bucket]/[path_to_json].json).

    Returns:
        Python Dictionary: A Python dictionary of the JSON file is loaded into memory.

    """
    s3 = boto3.client('s3')

    print('Requesting JSON from: s3://{}/{}'.format(xia_bucket, path_to_json))
    response = s3.get_object(Bucket=xia_bucket, Key=path_to_json)
    content = response['Body']
    print('Data loaded succesfully from S3.')
    try:
        jsonObject = json.loads(content.read())
    except Exception as e:
        raise e
    return jsonObject

def generate_records(jsonDict):
    """ Creating Documents for Elasticsearch (XSE)

    After loading in the JSON object, this function reformats the JSON to be
    acceptable by Elasticsearch.

    Limitations: The current script is built specifically for the DAU metadata.
    This code will be updated based on requirements from additional metadata
    sources, such as edX.

    Args:
        jsonDict (dict): Dictionary of a JSON list of metadata for courses.

    Returns:
        Generator: A generator of python dictionaries.

    """
    # creating a rough 'index' of the python dict object, we'll use this to iterate
    # through to identify the 1.) ID and 2.) course content
    iter_courses = tuple(jsonDict.items())

    # parse the number of record limit for the 'for' loop
    num_course = len(iter_courses)

    for course in range(0, num_course):
        c_id = iter_courses[course][0]
        # establishing the dict with the ID key value from the JSON
        doc = {
            "_id": c_id
        }
        c_response = iter_courses[course][1]

        # updating the dict to include the response object 'Course' and 'Lifecyle'
        doc.update(c_response)
        yield(doc)

def main(es_index, my_s3_bucket, my_json_file):
    # NOTE: Function assumes that the elasticsearch index has been created.
    # If one hasn't been created, please create one prior to executing this
    # function.
    print('Loading data from S3...')
    json_obj = source_json_data(xia_bucket=my_s3_bucket, path_to_json=my_json_file)
    print('Data loaded successfully.')

    number_of_docs = len(json_obj)
    client = Elasticsearch("10.0.0.4:9200") #update based on ES env parameters

    print('Starting indexing courses...')
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0

    for ok, action in streaming_bulk(
        client=client, index=es_index, actions=generate_records(jsonDict=json_obj),
    ):
        progress.update(1)
        successes += ok
    print("Indexed {}/{} documents".format(successes, number_of_docs))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
