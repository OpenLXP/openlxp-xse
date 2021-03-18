#!/bin/bash

## Tips to run: execute this file with '. ./xse_filter_parse.sh'

set -a # automatically export all variables
source .env # UPDATE: need to specify '.env' file within directory for variables below
set +a

DEPARTMENT_NAME=$(curl -X GET "${ES_SERVER}/${ES_INDEX}/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": { "XSEFilters": { "terms": { "field": "Course.DepartmentName.keyword" } } }
  }
')
COURSE_PROVIDER=$(curl -X GET "${ES_SERVER}/${ES_INDEX}/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": { "XSEFilters": { "terms": { "field": "Course.CourseProviderName.keyword" } } }
  }
')

unset DEPARTMENT_FILTER # clearing out potentially any left over variable / array
unset COURSE_PROVIDER_FILTER # clearing out potentially any left over variable / array

while read -r key; do
    DEPARTMENT_FILTER+=($key)
done <<< "$(jq -r '.aggregations.XSEFilters.buckets[].key' <<< "$DEPARTMENT_NAME")"

while read -r key; do
    COURSE_PROVIDER_FILTER+=($key)
done <<< "$(jq -r '.aggregations.XSEFilters.buckets[].key' <<< "$COURSE_PROVIDER")"

export DEPARTMENT_FILTER
export COURSE_PROVIDER_FILTER
