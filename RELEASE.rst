RELEASE_TYPE: major

Replacing the DynamoImageFactory and DynamoImage classes with DynamoEventFactory and DynamoEvent

- Perform quite a bit of sanity checking on event object received
- DynamoEvent can:
  - return old and new images (if available)
  - return modified keys only
  - return deserialized or otherwise images and keys based on params
