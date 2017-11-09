aws_utils
=========

This module is a collection of AWS-related utilities that we wrote while working on the Wellcome Digital Platform.

Some of these utilities are very specific to Wellcome projects, others are more generic and should be generally useful.

Documentation is available at `http://wellcome-aws-utils.readthedocs.io/ <http://wellcome-aws-utils.readthedocs.io/>`_.

Installation
************

You can install wellcome_aws_utils from PyPI::

   $ pip install wellcome_aws_utils

Note that this package **only supports Python 3.6 or later.**
It was originally written to run inside the AWS Lambda environment, which supports 2.7 or 3.6 --- and we make heavy use of f-strings, which are 3.6 only.

License
*******

MIT.
