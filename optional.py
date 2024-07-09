"""

This example is an Optional type which treats validation errors as a None value.

"""

from typing import Any, Annotated

from pydantic import BaseModel, ValidationError, TypeAdapter
from pydantic.functional_validators import WrapValidator
from pydantic_core.core_schema import ValidatorFunctionWrapHandler, ValidationInfo


class Child(BaseModel):
    number: int | None


def optional_type_validation_wrapper(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> int | None:
    """Wrap Pydantic's validation in a try/except, and return None on ValidationError."""
    try:
        return handler(v)
    except ValidationError:
        return None


OptionalChild = Annotated[Child, WrapValidator(optional_type_validation_wrapper)]


class Parent(BaseModel):
    children: list[OptionalChild]


parent_type_adapter = TypeAdapter(Parent)

input = {"children": [{"number": 0}, {"number": 1}, {"number": "two"}, {"number": 3}]}

parent = parent_type_adapter.validate_python(input)

assert parent == Parent(
    children=[
        Child(number=0),
        Child(number=1),
        None,
        Child(number=3),
    ]
)
