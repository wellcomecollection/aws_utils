RELEASE_TYPE: minor

Deprecates extract_json_message in favour of extract_sns_messages_from_lambda_event

extract_sns_messages_from_lambda_event provides:
- better sanity checking of event
- loops over available records
- returns subject along with json.load'ed message