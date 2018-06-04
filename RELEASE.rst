RELEASE_TYPE: patch

Previously sending a message with ``sns_utils.publish_sns_message`` would
log the entire SNS response.

Now the response is only logged if the SNS message is unsuccessful.
