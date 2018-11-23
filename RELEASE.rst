RELEASE_TYPE: patch

A large number of records in the Sierra VHS contain a ``reindexShard`` parameter which is not expected when initialising a ``HybridRecord()`` object. ``attrs`` can't handle data it doesn't expect, and the records with ``reindexShard`` parameters therefore fail to pass through the pipeline.

We now throw away any unnecessary data in the received message, allowing originally dirty messages to pass through without issue.