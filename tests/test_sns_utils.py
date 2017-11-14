# -*- encoding: utf-8 -*-

from datetime import datetime
import json

import boto3

from wellcome_aws_utils import sns_utils


def test_publish_sns_message(sns_sqs):
    sns_client = boto3.client('sns')
    sqs_client = boto3.client('sqs')
    topic_arn, queue_url = sns_sqs

    test_message = {
        'string': 'a',
        'number': 1,
        'date': datetime.strptime(
            'Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'
        )
    }

    expected_decoded_message = {
        'string': 'a',
        'number': 1,
        'date': '2005-06-01T13:33:00'
    }

    sns_utils.publish_sns_message(sns_client, topic_arn, test_message)

    messages = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )

    message_body = messages['Messages'][0]['Body']

    inner_message = json.loads(message_body)['Message']
    actual_decoded_message = json.loads(inner_message)

    assert (
        json.loads(actual_decoded_message['default']) ==
        expected_decoded_message)


def test_extract_json_message():
    example_object = {
        "foo": "bar",
        "baz": ["bat", 0, 0.1, {"boo": "beep"}]
    }

    example_object_json = json.dumps(example_object)

    example_event = {
        "Records": [
            {
                "Sns": {
                    "Message": example_object_json
                }

            }
        ]
    }

    extracted_object = sns_utils.extract_json_message(example_event)

    assert example_object == extracted_object


def test_extract_sns_messages_from_lambda_event():
    expected_subject = 'my_subject'
    expected_message = {
        "foo": "bar",
        "baz": ["bat", 0, 0.1, {"boo": "beep"}]
    }

    expected_message_json = json.dumps(expected_message)

    example_event = {
        "Records": [
            {
                "EventSource": 'aws:sns',
                "Sns": {
                    "Message": expected_message_json,
                    "Subject": expected_subject
                }

            }
        ]
    }

    actual_extracted_message = (
        sns_utils.extract_sns_messages_from_lambda_event(example_event)
    )

    assert list(actual_extracted_message) == [sns_utils.SNSEvent(
        message=expected_message,
        subject=expected_subject
    )]
