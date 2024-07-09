"""

This example is a list which filters out None values on validation.

"""

from typing import Annotated

from pydantic import WrapValidator, BaseModel, TypeAdapter
from pydantic_core.core_schema import ValidatorFunctionWrapHandler, ValidationInfo


def filtered_list_type_validation_wrapper(
    v: list, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> int | None:
    """Filter None values from a list."""
    if not isinstance(v, list):
        # let pydantic handle it
        return handler(v)

    return handler([i for i in v if i is not None])


class Child(BaseModel):
    number: int


FilteredList = Annotated[
    list[Child], WrapValidator(filtered_list_type_validation_wrapper)
]


class Parent(BaseModel):
    children: FilteredList


parent_type_adapter = TypeAdapter(Parent)

input = {
    "children": [
        {
            "number": 0,
        },
        {"number": 1},
        None,
        {"number": 3},
    ]
}
parent = parent_type_adapter.validate_python(input)

assert parent == Parent(children=[Child(number=0), Child(number=1), Child(number=3)])
