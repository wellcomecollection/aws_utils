RELEASE_TYPE: minor

This release adds utils for the reporting pipeline. 

The functions under ``reporting_utils.py`` describe a basic ETL pipeline from VHS to elasticsearch, without a transformation specified. In this way, the shape of the pipeline remains independent of both the data within it and the transforms being applied. 

As further data sources are added to the reporting pipeline and more lambdas are created, we keep repeated code to a minimum. In a new lambda, the user should specify a set of data-source-specific transformations in a ``transform.py`` file. The lambda's ``main`` can then remain minimal and generic:

.. code-block:: python
    from wellcome_aws_utils.reporting_utils import process_messages
    from transform import transform


    def main(event, _, s3_client=None, es_client=None, index=None, doc_type=None):
        process_messages(event, transform, s3_client, es_client, index, doc_type)
