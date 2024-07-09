"""

This example is a list which filters out items that fail validation. 
It uses the optional wrapper inside a variation on the filtered list wrapper.

"""

from typing import Annotated

from pydantic import WrapValidator, BaseModel, TypeAdapter
from pydantic_core.core_schema import ValidatorFunctionWrapHandler, ValidationInfo

from optional import optional_type_validation_wrapper


class Child(BaseModel):
    number: int


# this type transforms validation failure into a None value

OptionalChild = Annotated[Child, WrapValidator(optional_type_validation_wrapper)]


def filtered_list_type_validation_wrapper(
    v: list, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> list:
    """Filter None values from a list."""
    # in this variation on the filtered list, pydantic performs its
    # validation first, so we have a list of successfully validated
    # objects mixed with None which replaced failed validations.
    validated_list = handler(v)

    return [i for i in validated_list if i is not None]


ValidatedList = Annotated[
    list[OptionalChild], WrapValidator(filtered_list_type_validation_wrapper)
]


class Parent(BaseModel):
    children: ValidatedList


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


assert parent == Parent(
    children=[
        Child(number=0),
        Child(number=1),
        Child(number=3),
    ]
)
