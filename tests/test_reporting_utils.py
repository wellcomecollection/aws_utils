import json
import boto3
from moto import mock_s3
from unittest.mock import patch
from wellcome_aws_utils.reporting_utils import process_messages


def create_sns_message(bucket_name, id, key):
    return {
        "Records": [
            {
                "Sns": {
                    "Message": (f'{{"id":"{id}","version":1,"location":'
                                f'{{"namespace":"{bucket_name}","'
                                f'key":"{key}"}}}}'),
                    "MessageAttributes": {},
                    "MessageId": "0cf7d798-64c8-45a7-a7bf-a9ebc94d1108",
                    "Type": "Notification",
                }
            }
        ]
    }


def given_s3_has(s3_client, bucket, key, data):
    s3_client.put_object(
        ACL="public-read",
        Bucket=bucket,
        Key=key,
        Body=data,
        CacheControl="max-age=0",
        ContentType="application/json",
    )


def identity_transform(record):
    return record


class TestReportingUtils(object):
    @mock_s3
    def test_saves_record_in_es(self):
        with patch('elasticsearch.Elasticsearch') as MockElasticsearch:
            id = "V0000001"
            mock_elasticsearch_client = MockElasticsearch()
            elasticsearch_index = "index"
            elasticsearch_doctype = "example"
            hybrid_data = '{"foo": "bar"}'
            key = "00/V0000001/0.json"
            bucket = "bukkit"

            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket)
            given_s3_has(
                s3_client=s3_client,
                bucket=bucket,
                key=key,
                data=json.dumps(hybrid_data)
            )

            event = create_sns_message(bucket, id, key)

            process_messages(
                event,
                identity_transform,
                s3_client,
                mock_elasticsearch_client,
                elasticsearch_index,
                elasticsearch_doctype,
            )

            mock_elasticsearch_client.index.assert_called_once_with(
                body=hybrid_data,
                doc_type=elasticsearch_doctype,
                id=id,
                index=elasticsearch_index
            )
