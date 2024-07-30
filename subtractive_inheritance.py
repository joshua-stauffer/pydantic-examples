"""

This example is a utility which creates a new model based on an existing one without a given field.

"""

from typing import TypeVar

from pydantic import BaseModel, create_model

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def create_model_without_fields(
    model: type[BaseModel], class_name: str, exclude_fields: set[str]
):
    # this manipulation of pydantic internals was adapted from an example
    # given by a project maintainer. I've updated it to work with V2.
    # https://github.com/pydantic/pydantic/issues/2272#issuecomment-771205557
    all_annotations = {}
    for base in reversed(model.__bases__):
        all_annotations.update(getattr(base, "__annotations__", {}))
    all_annotations.update(model.__annotations__)

    field_definitions = {}

    for field_name, field in model.__fields__.items():
        if field_name in exclude_fields:
            continue
        field_definitions[field_name] = (all_annotations.get(field_name), field)

    return create_model(class_name, **field_definitions)


class Parent(BaseModel):
    id: int
    name: str


Child = create_model_without_fields(
    model=Parent, class_name="Child", exclude_fields={"id"}
)


class ChildWithID(Child):
    id: int


Parent(id=1, name="parent")
Child(name="child")
ChildWithID(name="child", id=1)
