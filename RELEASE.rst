RELEASE_TYPE: minor

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
