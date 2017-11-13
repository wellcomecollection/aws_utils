# -*- encoding: utf-8 -*-

import datetime
import decimal
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            if float(obj).is_integer():
                return int(obj)
            else:
                return float(obj)

        return json.JSONEncoder.default(self, obj)


def publish_sns_message(sns_client,
                        topic_arn,
                        message,
                        subject="default-subject"):
    """
    Given a topic ARN and a series of key-value pairs, publish the key-value
    data to the SNS topic.
    """
    response = sns_client.publish(
        TopicArn=topic_arn,
        MessageStructure='json',
        Message=json.dumps({
            'default': json.dumps(
                message,
                cls=EnhancedJSONEncoder
            )
        }),
        Subject=subject
    )

    print(f'SNS response = {response!r}')
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    return response


def extract_sns_messages_from_lambda_event(event):
    """
    Extracts a JSON message from an SNS event sent to a lambda

    """
    if 'Records' not in event:
        raise Exception(f'No records found in {event}')

    messages = []
    for record in event['Records']:
        if record['EventSource'] != 'aws:sns':
            raise Exception(f'Invalid message source for {record}')

        if ('Sns' not in record) or ('Message' not in record['Sns']) or ('Subject' not in record['Sns']):
            raise Exception(f'Invalid message structure for {record}')

        subject = record['Sns']['Subject']
        message = json.loads(record['Sns']['Message'])

        messages.append({
            'subject': subject,
            'message': message
        })

    return messages


def extract_json_message(event):
    """
    Extracts a JSON message from an SNS event sent to a lambda

    Deprecated in favour of extract_sns_messages_from_lambda_event
    """
    message = event['Records'][0]['Sns']['Message']
    return json.loads(message)
