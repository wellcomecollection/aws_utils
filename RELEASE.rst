RELEASE_TYPE: minor

Deprecates ``sns_utils.extract_json_message`` in favour of ``sns_utils.extract_sns_messages_from_lambda_event``.

extract_sns_messages_from_lambda_event provides:
- better error reporting if the event is malformed
- loops over all available records from event not just the first
- returns subject along with the json decoded message

This release also adds ``UnWellcomeException`` which will be used as the base exception for new errors.