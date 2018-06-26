RELEASE_TYPE: patch

Previously sending a message with ``sns_utils.publish_sns_message`` would
print a message upon success.

Now this message is only logged at debug level.
