# -*- encoding: utf-8

from wellcome_aws_utils import lambda_utils as lu


@lu.log_on_error
def return_2():
    return 2


def test_log_on_error_preserves_return_value():
    assert return_2() == 2
