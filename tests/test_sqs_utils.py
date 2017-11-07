# -*- encoding: utf-8 -*-

import logging

import boto3
import daiquiri
from moto import mock_sqs
import pytest

from wellcome_aws_utils import sqs_utils


daiquiri.setup(level=logging.INFO)

logger = daiquiri.getLogger(__name__)


@pytest.fixture
def queue_url():
    with mock_sqs():
        client = boto3.client('sqs')
        resp = client.create_queue(QueueName='TestQueue')
        logger.info('%r', resp)
        yield resp['QueueUrl']
        client.delete_queue(QueueUrl=resp['QueueUrl'])


@pytest.mark.parametrize('kwargs', [
    {},
    {'delete': False},
    {'delete': True},
    {'batch_size': 1},
    {'batch_size': 10},
    {'delete': True, 'batch_size': 2},
    {'delete': False, 'batch_size': 7},
])
def test_get_empty_queue_is_empty(queue_url, kwargs):
    assert list(sqs_utils.get_messages(queue_url, **kwargs)) == []
