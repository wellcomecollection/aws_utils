RELEASE_TYPE: minor

This release modifies the way that secrets are handled by lambdas in the reporting pipleine. Previously, secrets were passed to lambdas as environment variables, defined in terraform. We now fetch secrets from AWS secretsmanager as records move through the pipeline.
