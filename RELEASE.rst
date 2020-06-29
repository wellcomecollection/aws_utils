RELEASE_TYPE: minor

The adapters now only send an ID / Version, and we need to look that up in Dynamo to fetch the S3 object in the reporting code.
