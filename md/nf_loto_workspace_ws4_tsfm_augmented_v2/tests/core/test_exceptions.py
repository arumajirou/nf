from nf_loto_platform.core import exceptions


def test_exceptions_are_subclasses_of_exception():
    assert issubclass(exceptions.ConfigError, Exception)
    assert issubclass(exceptions.DataError, Exception)
    assert issubclass(exceptions.RunError, Exception)
