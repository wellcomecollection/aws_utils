RELEASE_TYPE: patch

This fixes a bug in the ``@log_on_error`` decorator where the return value
of the original function would be replaced by ``None``.  This decorator now
preserves the original return value.