# OpenLXP - Experience Search Engine (XSE)

This directory contains the code to install, configure, and run a search engine to support the OpenLXP platform.

## Intended use

Intended use of this code is that a user could reference this code and architecture as boilerplate code to stand-up a search engine for their learning experience platform on OpenLXP.

## Capabilities and limitations

The code in this repository leverages AWS infrastructure for hosting. Ideally, the code can be modified to run on any major cloud platform with parameter tweaks, but has not been verified. Additionally, the code within this repository is specifically for [Elasticsearch 7.11](https://www.elastic.co/guide/en/elasticsearch/reference/7.11/getting-started.html) as the search engine. We are utilizing Elasticsearch (ES) for representative purposes, users can leverage an additional search engine as it fits their budget and architecture.

The helper script to load data from S3 into the ES instance has been tested with Python 3.6. Please ensure you have Python >=3.6 installed before executing the script.

## Directions for use

Clone the OpenLXP git repo onto your local machine:
```console
git clone https://github.com/OpenLXP/openlxp-xse.git
```

**TO-DO: Build out docker compose / cluster configuration to bootstrap the installation and configuration of the cluster.**

====After ES cluster is stood up====

To verify the cluster is running, run the below curl command from your Linux terminal or Windows CMD prompt. Note: you may need to update the 'Security Group' of your Elasticsearch EC2 instance to accept traffic on port 9200 from your IP address. Search 'whats my IP' in Google or your favorite serach engine to find out your local IP address.
```console
curl -X GET "[public-ip-address-of-EC2-ES]:9200/_cat/health?v=true&pretty"
```

Next, we will index a set of sample documents from an S3 bucket into the ES instance. To assist with this process, we'll use a sample pipeline that takes processed DAU data from XIS/XIA and configures into the format ES is expecting.

Within your terminal (Linux or CMD), navigate to the `src` folder. Once in the `src` folder, run the below command to install necessary python packages to execute the script:
```console
python3 pip3 install -r requirements.txt
```

Next, run the following command edit the document using 'nano' or a similar text editor:
```console
nano es-doc-gen.py
```

Within the `es-doc-gen.py` file, update the IP address for your ES instance and save the document. Be sure to use the *Public IP address* for the ES instance, which you can confirm on the AWS Console. Back on the terminal, update `my-index-name` `my-s3-bucket-name` `sample-DAU-data.json` to match the names of the index, S3 bucket, and JSON file of the sample DAU data. After doing so, run the following command:
```console
python3 es-doc-gen.py 'my-index-name' 'my-s3-bucket-name' 'sample-DAU-data.json'
```

Success! You've now indexed sample course data into ES and it's ready to be queried. To verify the data has been loaded into ES correctly, try running the following script from your terminal:
```console
curl -X GET "[public-ip-address-of-EC2-ES]:9200/[my-index-name]/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match": { "Course.CourseDescription": "and service" } }
}
'
```

Congratulations, you've installed and configured an ES cluster, indexed sample documents, and conducted a sample query on your ES instance. Happy searching!
## Further resources

For more details on Elasticsearch, please refer to the following documentation:
* [Elasticsearch - What is Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.11/elasticsearch-intro.html)
