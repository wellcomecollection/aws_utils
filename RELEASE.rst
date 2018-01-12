RELEASE_TYPE: patch

This fixes a bug in ``s3_utils.parse_s3_record``.  If the key of a changed
file included a character which is usually quoted in URLs (e.g. ``+``),
a parsed record from the S3 event stream would use the URL-quoted form
of the object key.

For example, a change to ``s3://example/foo+bar`` would become ``foo%2Bbar``.

This version unquotes the key when parsing the event.
