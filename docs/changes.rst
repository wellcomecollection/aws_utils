=========
Changelog
=========

This is a record of all releases of wellcome_aws_utils.

------------------
2.1.1 - 2018-06-04
------------------

Now ``@log_on_error`` can be used to decorate functions with arbitrary arguments/keyword arguments.

------------------
2.1.0 - 2018-06-04
------------------

This adds a new method: ``lambda_utils.log_on_error``.  This can be used to
decorate the main function for a Lambda, and logs the event/context if the
Lambda throws an unexpected exception.

For example, running the following snippet:

.. code-block:: python

   @log_on_error
   def handler(event, context=None):
       if event == {1: '1', 2: '2'}:
           raise ValueError


   handler(event={'foo': 'bar'})
   handler(event='99 green bottles' * 99)
   handler(event={1: '1', 2: '2'})

gives the following output:

.. code-block::

   event   = {1: '1', 2: '2'}
   context = None

   ValueError:
     module body in lambda_utils.py at line 30
       handler(event={1: '1', 2: '2'}, context=None)
     function wrapper in lambda_utils.py at line 13
       fn(event, context)
     function handler in lambda_utils.py at line 26
       raise ValueError

This makes it easier to debug failed Lambdas, but without the expense of
logging every event that a Lambda receives.

------------------
2.0.2 - 2018-06-04
------------------

Previously sending a message with ``sns_utils.publish_sns_message`` would
log the entire SNS response.

Now the response is only logged if the SNS message is unsuccessful.

------------------
2.0.1 - 2018-01-12
------------------

This fixes a bug in ``s3_utils.parse_s3_record``.  If the key of a changed
file included a character which is usually quoted in URLs (e.g. ``+``),
a parsed record from the S3 event stream would use the URL-quoted form
of the object key.

For example, a change to ``s3://example/foo+bar`` would become ``foo%2Bbar``.

This version unquotes the key when parsing the event.

------------------
2.0.0 - 2017-11-29
------------------

Replacing the DynamoImageFactory and DynamoImage classes with DynamoEventFactory and DynamoEvent

- Perform quite a bit of sanity checking on event object received
- DynamoEvent can:
  - return old and new images (if available)
  - return modified keys only
  - return deserialized or otherwise images and keys based on params

------------------
1.1.0 - 2017-11-15
------------------

Deprecates ``sns_utils.extract_json_message`` in favour of ``sns_utils.extract_sns_messages_from_lambda_event``.

extract_sns_messages_from_lambda_event provides:
- better error reporting if the event is malformed
- loops over all available records from event not just the first
- returns subject along with the json decoded message

This release also adds ``UnWellcomeException`` which will be used as the base exception for new errors.

------------------
1.0.0 - 2017-11-07
------------------

First production release!
