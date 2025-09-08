from src.schemas_base import AtLeastOneFieldRequired
import pytest
from pydantic import ValidationError


def test_should_raise_if_not_defined_required_fields() -> None:
    """Generate raise need to specify required fields"""

    class WrongClass(AtLeastOneFieldRequired):
        field1: int
        field2: str

    with pytest.raises(NotImplementedError):
        WrongClass(field1=1, field2="String")


def test_should_correct_raise_exception_if_all_option_is_none() -> None:
    class ClassWithSomeOptional(AtLeastOneFieldRequired):
        field1: str
        _required_fields = ("opt_field1", "opt_field2")

        opt_field1: str | None = None
        opt_field2: str | None = None
        opt_field3: str | None = None

    ClassWithSomeOptional(field1="some field", opt_field1="data")  # correct
    with pytest.raises(ValidationError):
        ClassWithSomeOptional(field1="some field", opt_field3="data")  # incorrect need opt_field2 or opt_field1
