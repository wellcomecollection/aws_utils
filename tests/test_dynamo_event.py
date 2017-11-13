# -*- encoding: utf-8 -*-

from wellcome_aws_utils import dynamo_event

event_source_arn = (
    "arn:aws:dynamodb:us-east-1:123456789012:"
    "table/BarkTable/stream/2016-11-16T20:42:48.104"
)


def create_insert_record(message):
    return {
        "ApproximateCreationDateTime": 1479499740,
        "Keys": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "NewImage": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Message": {
                "S": message
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "SequenceNumber": "13021600000000001596893679",
        "SizeBytes": 112,
        "StreamViewType": "NEW_IMAGE"
    }


def create_remove_record(message):
    return {
        "ApproximateCreationDateTime": 1479499740,
        "Keys": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "OldImage": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Message": {
                "S": message
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "SequenceNumber": "13021600000000001596893679",
        "SizeBytes": 112,
        "StreamViewType": "OLD_IMAGE"
    }


def create_modify_record(old_message, new_message):
    return {
        "ApproximateCreationDateTime": 1479499740,
        "Keys": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "OldImage": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Message": {
                "S": old_message
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "NewImage": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Message": {
                "S": new_message
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "SequenceNumber": "13021600000000001596893679",
        "SizeBytes": 112,
        "StreamViewType": "NEW_AND_OLD_IMAGES"
    }


def create_modify_record_keys_only():
    return {
        "ApproximateCreationDateTime": 1479499740,
        "Keys": {
            "Timestamp": {
                "S": "2016-11-18:12:09:36"
            },
            "Username": {
                "S": "John Doe"
            }
        },
        "SequenceNumber": "13021600000000001596893679",
        "SizeBytes": 112,
        "StreamViewType": "KEYS_ONLY"
    }


def create_insert_event(message):
    return {
        "eventID": "7de3041dd709b024af6f29e4fa13d34c",
        "eventName": "INSERT",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": create_insert_record(message),
        "eventSourceARN": event_source_arn
    }


def create_remove_event(message):
    return {
        "eventID": "7de3041dd709b024af6f29e4fa13d34c",
        "eventName": "REMOVE",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": create_remove_record(message),
        "eventSourceARN": event_source_arn
    }


def create_modify_event(old_message, new_message):
    return {
        "eventID": "7de3041dd709b024af6f29e4fa13d34c",
        "eventName": "MODIFY",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": create_modify_record(old_message, new_message),
        "eventSourceARN": event_source_arn
    }


def create_modify_event_keys_only():
    return {
        "eventID": "7de3041dd709b024af6f29e4fa13d34c",
        "eventName": "MODIFY",
        "eventVersion": "1.1",
        "eventSource": "aws:dynamodb",
        "awsRegion": "us-west-2",
        "dynamodb": create_modify_record_keys_only(),
        "eventSourceARN": event_source_arn
    }


def test_get_source_arn():
    dynamo_image = dynamo_utils.DynamoEvent(create_insert_event('foo'))
    assert dynamo_image.event_source_arn == event_source_arn


def test_insert_event():
    dynamo_image = dynamo_utils.DynamoEvent(create_insert_event('foo'))

    expected_image_with_deserialized_values = {
        'Message': 'foo',
        'Timestamp': '2016-11-18:12:09:36',
        'Username': 'John Doe'
    }

    expected_image = {
        "Timestamp": {
            "S": "2016-11-18:12:09:36"
        },
        "Message": {
            "S": 'foo'
        },
        "Username": {
            "S": "John Doe"
        }
    }

    assert dynamo_image.new_image(
        deserialize_values=True
    ) == expected_image_with_deserialized_values

    assert dynamo_image.new_image() == expected_image


def test_remove_event():
    dynamo_image = dynamo_utils.DynamoEvent(create_remove_event('foo'))

    expected_image_with_deserialized_values = {
        'Message': 'foo',
        'Timestamp': '2016-11-18:12:09:36',
        'Username': 'John Doe'
    }

    expected_image = {
        "Timestamp": {
            "S": "2016-11-18:12:09:36"
        },
        "Message": {
            "S": 'foo'
        },
        "Username": {
            "S": "John Doe"
        }
    }

    assert dynamo_image.new_image(deserialize_values=True) is None
    assert dynamo_image.new_image() is None

    assert dynamo_image.old_image(
        deserialize_values=True
    ) == expected_image_with_deserialized_values
    assert dynamo_image.old_image() == expected_image


def test_modify_event():
    dynamo_image = dynamo_utils.DynamoEvent(create_modify_event('foo', 'bar'))

    expected_old_image_with_deserialized_values = {
        'Message': 'foo',
        'Timestamp': '2016-11-18:12:09:36',
        'Username': 'John Doe'
    }

    expected_old_image = {
        "Timestamp": {
            "S": "2016-11-18:12:09:36"
        },
        "Message": {
            "S": 'foo'
        },
        "Username": {
            "S": "John Doe"
        }
    }

    expected_new_image_with_deserialized_values = {
        'Message': 'bar',
        'Timestamp': '2016-11-18:12:09:36',
        'Username': 'John Doe'
    }

    expected_new_image = {
        "Timestamp": {
            "S": "2016-11-18:12:09:36"
        },
        "Message": {
            "S": 'bar'
        },
        "Username": {
            "S": "John Doe"
        }
    }

    assert dynamo_image.new_image(
        deserialize_values=True
    ) == expected_new_image_with_deserialized_values
    assert dynamo_image.new_image() == expected_new_image

    assert dynamo_image.old_image(
        deserialize_values=True
    ) == expected_old_image_with_deserialized_values
    assert dynamo_image.old_image() == expected_old_image


def test_modify_event_keys_only():
    dynamo_image = dynamo_utils.DynamoEvent(create_modify_event_keys_only())

    assert dynamo_image.new_image(deserialize_values=True) is None
    assert dynamo_image.new_image() is None

    assert dynamo_image.old_image(deserialize_values=True) is None
    assert dynamo_image.old_image() is None

    assert dynamo_image.keys(deserialize_values=True) == {
        'Timestamp': '2016-11-18:12:09:36',
        'Username': 'John Doe'
    }
    assert dynamo_image.keys() == {
        "Timestamp": {
            "S": "2016-11-18:12:09:36"
        },
        "Username": {
            "S": "John Doe"
        }
    }
