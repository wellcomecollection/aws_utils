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
