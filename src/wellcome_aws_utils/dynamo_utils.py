# -*- encoding: utf-8 -*-

from enum import Enum

from boto3.dynamodb.types import TypeDeserializer


class DynamoEventFactory:
    @staticmethod
    def create(event):
        return [DynamoEvent(record) for record in event['Records']]


class DynamoEventType(Enum):
    REMOVE, INSERT, MODIFY = range(3)


class DynamoEvent:
    def _sanity_check_record(self, record):
        if not ('eventSource' in record):
            raise Exception(f'Unrecognised event: {record}')

        if record['eventSource'] != 'aws:dynamodb':
            raise Exception(f'Event source is not aws:dynamodb: {record}')

    def _set_event_type(self, record):
        if 'eventName' not in record:
            raise Exception(f'No eventName found in {record}!')

        self.event_type = None
        if self.record['eventName'] == 'REMOVE':
            self.event_type = DynamoEventType.REMOVE

        if self.record['eventName'] == 'INSERT':
            self.event_type = DynamoEventType.INSERT

        if self.record['eventName'] == 'MODIFY':
            self.event_type = DynamoEventType.MODIFY

        if self.event_type is None:
            raise Exception(
                f'Unrecognised eventName found in {record}!'
            )

    def _set_event_source_arn(self, record):
        if 'eventSourceARN' not in record:
            raise Exception(
                f'No eventSourceARN attribute available on record: {record}'
            )

        self.event_source_arn = record['eventSourceARN']

    def _extract_dynamodb_from_record(self, record):
        if 'dynamodb' not in record:
            raise Exception(
                f'No dynamodb attribute available on record: {record}'
            )

        return record['dynamodb']

    def _set_keys(self, dynamodb):
        if 'Keys' not in dynamodb:
            raise Exception(
                f'No Keys attribute available on record.dynamodb: {dynamodb}'
            )

        self._keys = dynamodb['Keys']

    def _set_images(self, dynamodb):
        new_image = None
        if 'NewImage' in dynamodb:
            new_image = dynamodb['NewImage']

        old_image = None
        if 'OldImage' in dynamodb:
            old_image = dynamodb['OldImage']

        self._new_image = new_image
        self._old_image = old_image

    def __init__(self, record):
        self.record = record

        self._sanity_check_record(record)
        self._set_event_type(record)
        self._set_event_source_arn(record)

        dynamodb = self._extract_dynamodb_from_record(record)

        self._set_keys(dynamodb)
        self._set_images(dynamodb)

    @staticmethod
    def _deserialize_values(image):
        td = TypeDeserializer()
        return {k: td.deserialize(v) for k, v in image.items()}

    def keys(self, deserialize_values=False):
        if deserialize_values and self._keys:
            return DynamoEvent._deserialize_values(self._keys)

        return self._keys

    def new_image(self, deserialize_values=False):
        if deserialize_values and self._new_image:
            return DynamoEvent._deserialize_values(self._new_image)

        return self._new_image

    def old_image(self, deserialize_values=False):
        if deserialize_values and self._old_image:
            return DynamoEvent._deserialize_values(self._old_image)

        return self._old_image


def _is_capacity_different(x, desired_capacity):
    read_capacity_units = x['ProvisionedThroughput']['ReadCapacityUnits']
    write_capacity_units = x['ProvisionedThroughput']['WriteCapacityUnits']
    return (
        read_capacity_units != desired_capacity
    ) or (
        write_capacity_units != desired_capacity
    )


def change_dynamo_capacity(client, table_name, desired_capacity):
    """
    Given the name of a DynamoDB table and a desired capacity, update the
    read/write capacity of the table and every secondary index.
    """

    response = client.describe_table(TableName=table_name)

    filtered_gsis = filter(
        lambda x: _is_capacity_different(x, desired_capacity),
        response['Table']['GlobalSecondaryIndexes'])

    gsi_updates = list(map(
        lambda x: {
            'Update': {
                'IndexName': x['IndexName'],
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': desired_capacity,
                    'WriteCapacityUnits': desired_capacity
                }
            }
        },
        filtered_gsis
    ))

    table_update = _is_capacity_different(response['Table'], desired_capacity)
    print(f'table_update: {table_update}')

    if gsi_updates and table_update:
        resp = client.update_table(
            TableName=table_name,
            ProvisionedThroughput={
                'ReadCapacityUnits': desired_capacity,
                'WriteCapacityUnits': desired_capacity
            },
            GlobalSecondaryIndexUpdates=gsi_updates
        )
    elif gsi_updates:
        resp = client.update_table(
            TableName=table_name,
            GlobalSecondaryIndexUpdates=gsi_updates
        )
    elif table_update:
        resp = client.update_table(
            TableName=table_name,
            ProvisionedThroughput={
                'ReadCapacityUnits': desired_capacity,
                'WriteCapacityUnits': desired_capacity
            }
        )
    else:
        return

    print(f'DynamoDB response = {resp!r}')
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
