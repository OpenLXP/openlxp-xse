import requests
import json

def generate_filters(es_uri, es_index, field):
    """ Generating filters from ES

    The objective of the function is pull available filter values from the
    Elasticsearch (ES) index. The user must specify a DNS or IP for the ES server,
    the target index, and the field which must be parsed.

    Limitations: The current script is built specifically for ES. Other search
    engines may have different syntax for REST API requests and response structure.
    Additionally, the ES field is only for 'Term' filtering; modifications will be needed
    to incorporate 'Range' values (e.g., Date, Time) in the future.

    Args:
        es_uri (str): DNS or IP address, with port (e.g., 192.0.0.2:9200), for the
        ES server.
        es_index (str): Name of index
        field (str): ES index mapping (Term) to the desired field used for filtering
        (e.g., 'Course.CourseProvider.keyword'). View the mapping of the target index
        to craft the field (https://www.elastic.co/guide/en/elasticsearch/reference/7.11/mapping.html)

    Returns:
        filter_val (list): A Python list of available filter values for the specified
        field.

    """

    headers = {"Content-Type": "application/json"}
    # specifying the framework for the ES payload to query available results
    payload = {"aggs": { "XSEFilters": { "terms": { "field": "" } } } }
    # updating the dict to include the user-specified field value
    payload['aggs']['XSEFilters']['terms'].update({"field": field})
    res = requests.get("http://"+es_uri+"/"+es_index+"/_search?pretty", headers=headers, data=json.dumps(payload))

    # parsing the response to pull the relevant response 'bucket' aggregation
    response_j = res.json()['aggregations']['XSEFilters']['buckets']
    num_filter = len(response_j)
    filter_val = []
    for value in range(0, num_filter):
        filter_val.append(response_j[value]['key'])

    return filter_val
