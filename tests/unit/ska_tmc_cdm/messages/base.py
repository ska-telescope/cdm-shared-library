# flake8: noqa
from datetime import datetime, timezone
from typing import Any, Callable, Optional

import pytest
from pydantic import AwareDatetime, Field

from ska_tmc_cdm import CdmObject

FIELD_NAME = "field"


class Obj(CdmObject):
    n: Optional[int] = None


DT = datetime(1985, 10, 17, tzinfo=timezone.utc)


def utcnow():
    return datetime.now(tz=timezone.utc)


def object_factory(
    annotation: type,
    value: Any = ...,
    static_default: Any = ...,
    default_factory: Optional[Callable] = None,
    exclude: bool | None = None,
):
    """
    This is a test utility that takes a type-annotation, a field value,
    and either a static or dynamic default for that field. It will
    create a new subclass of CdmObject, then instantiate and object
    and return it.

    We're using ... (the Python Ellipsis builtin) to mean "unset"
    because need to differentiate between absent/undefined and
    present-but-with-a-None values.

    Put another way, this function call:

    obj = object_factory(str, "world", static_default="hello")

    is equivalent to:

    class NewObj(CdmObject):
        field: str = "hello"

    obj = NewObj(field="world")
    """
    assert not (
        static_default is not Ellipsis and default_factory is not None
    ), "static_default and default_factory are mutually exclusive"
    # https://stackoverflow.com/a/75495929/845210
    class_constructor_args = {
        "__annotations__": {FIELD_NAME: annotation},
        FIELD_NAME: Field(
            static_default, default_factory=default_factory, exclude=exclude
        ),
    }

    NewObj = type(
        "NewObj",
        (CdmObject,),
        class_constructor_args,
    )
    if value is not Ellipsis:
        return NewObj(**{FIELD_NAME: value})
    return NewObj()


# fmt: off
FIELD_CASES = (
    # Scalar static value cases...
    pytest.param(object_factory(str,           static_default=...,  value="x"),  True, id="str|default:...|value:x"),
    pytest.param(object_factory(str,           static_default=...,  value=""),   True, id="str|default:...|value:''"),
    pytest.param(object_factory(Optional[str], static_default=None, value="x"),  True, id="Optional[str]|default:None|value:x"),
    pytest.param(object_factory(Optional[str], static_default=None, value=...),  False, id="Optional[str]|default:None|value:..."),
    pytest.param(object_factory(Optional[str], static_default=None, value=None), False, id="Optional[str]|default:None|value:None"),
    pytest.param(object_factory(Optional[str], static_default="x",  value="x"),  True, id="Optional[str]|default:x|value:x"),
    pytest.param(object_factory(Optional[str], static_default="x",  value=...),  True, id="Optional[str]|default:x|value:..."),
    pytest.param(object_factory(Optional[str], static_default="x",  value=None), True, id="Optional[str]|default:x|value:None"),
    # Scalar dynamic value cases...
    pytest.param(object_factory(AwareDatetime,           static_default=...,     value=DT),   True, id="datetime|default:...|value:DT"),
    pytest.param(object_factory(Optional[AwareDatetime], static_default=None,    value=DT),   True, id="Optional[datetime]|default:None|value:DT"),
    pytest.param(object_factory(Optional[AwareDatetime], static_default=None,    value=...),  False, id="Optional[datetime]|default:None|value:..."),
    pytest.param(object_factory(Optional[AwareDatetime], static_default=None,    value=None), False, id="Optional[datetime]|default:None|value:None"),
    pytest.param(object_factory(Optional[AwareDatetime], default_factory=utcnow, value=DT),   True, id="Optional[datetime]|default:utcnow|value:DT"),
    pytest.param(object_factory(Optional[AwareDatetime], default_factory=utcnow, value=...),  True, id="Optional[datetime]|default:utcnow|value:..."),
    pytest.param(object_factory(Optional[AwareDatetime], default_factory=utcnow, value=None), True, id="Optional[datetime]|default:utcnow|value:None"),
    # List cases...
    pytest.param(object_factory(list[str],           static_default=...,            value=["x"]), True, id="list|default:...|value:[x]"),
    pytest.param(object_factory(list[str],           static_default=...,            value=[]),    True, id="list|default:...|value:[]"),
    pytest.param(object_factory(list[str],           default_factory=list,          value=["x"]), True, id="list|default:[]|value:[x]"),
    pytest.param(object_factory(list[str],           default_factory=list,          value=...),   False, id="list|default:[]]|value:..."),
    pytest.param(object_factory(list[str],           default_factory=list,          value=[]),    False, id="list|default:[]|value:[]"),
    pytest.param(object_factory(list[str],           default_factory=lambda: ["x"], value=["x"]), True, id="list|default:[x]|value:[x]"),
    pytest.param(object_factory(list[str],           default_factory=lambda: ["x"], value=...),   True, id="list|default:[x]|value:..."),
    pytest.param(object_factory(list[str],           default_factory=lambda: ["x"], value=[]),    True, id="list|default:[x]|value:[]"),
    pytest.param(object_factory(Optional[list[str]], static_default=...,            value=["x"]), True, id="Optional[list]|default:...|value:[x]"),
    pytest.param(object_factory(Optional[list[str]], static_default=...,            value=[]),    True, id="Optional[list]|default:...|value:[]"),
    pytest.param(object_factory(Optional[list[str]], static_default=...,            value=None),  True, id="Optional[list]|default:...|value:None"),
    pytest.param(object_factory(Optional[list[str]], static_default=None,           value=["x"]), True, id="Optional[list]|default:None|value:[x]"),
    pytest.param(object_factory(Optional[list[str]], static_default=None,           value=...),   False, id="Optional[list]|default:None]|value:..."),
    pytest.param(object_factory(Optional[list[str]], static_default=None,           value=[]),    True, id="Optional[list]|default:None|value:[]"),
    pytest.param(object_factory(Optional[list[str]], static_default=None,           value=None),  False, id="Optional[list]|default:None|value:None"),
    pytest.param(object_factory(Optional[list[str]], default_factory=list,          value=["x"]), True, id="Optional[list]|default:[]|value:[x]"),
    pytest.param(object_factory(Optional[list[str]], default_factory=list,          value=...),   False, id="Optional[list]|default:[]]|value:..."),
    pytest.param(object_factory(Optional[list[str]], default_factory=list,          value=[]),    False, id="Optional[list]|default:[]|value:[]"),
    pytest.param(object_factory(Optional[list[str]], default_factory=list,          value=None),  True, id="Optional[list]|default:[]|value:None"),
    pytest.param(object_factory(Optional[list[str]], default_factory=lambda: ["x"], value=["x"]), True, id="Optional[list]|default:[x]|value:[x]"),
    pytest.param(object_factory(Optional[list[str]], default_factory=lambda: ["x"], value=...),   True, id="Optional[list]|default:[x]|value:..."),
    pytest.param(object_factory(Optional[list[str]], default_factory=lambda: ["x"], value=[]),    True, id="Optional[list]|default:[x]|value:[]"),
    pytest.param(object_factory(Optional[list[str]], default_factory=lambda: ["x"], value=None),  True, id="Optional[list]|default:[x]|value:None"),
    # Dict cases...
    pytest.param(object_factory(dict[str, str],           static_default=...,                 value={"x": "y"}), True, id="dict|default:...|value:{x:y}"),
    pytest.param(object_factory(dict[str, str],           static_default=...,                 value={}),         True, id="dict|default:...|value:{}"),
    pytest.param(object_factory(dict[str, str],           default_factory=dict,               value={"x": "y"}), True, id="dict|default:{}|value:{x:y}"),
    pytest.param(object_factory(dict[str, str],           default_factory=dict,               value=...),        False, id="dict|default:{}]|value:..."),
    pytest.param(object_factory(dict[str, str],           default_factory=dict,               value={}),         False, id="dict|default:{}|value:{}"),
    pytest.param(object_factory(dict[str, str],           default_factory=lambda: {"x": "y"}, value={"x": "y"}), True, id="dict|default:{x:y}|value:{x:y}"),
    pytest.param(object_factory(dict[str, str],           default_factory=lambda: {"x": "y"}, value=...),        True, id="dict|default:{x:y}|value:..."),
    pytest.param(object_factory(dict[str, str],           default_factory=lambda: {"x": "y"}, value={}),         True, id="dict|default:{x:y}|value:{}"),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=...,                 value={"x": "y"}), True, id="Optional[dict|default:...|value:{x:y}"),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=...,                 value={}),         True, id="Optional[dict|default:...|value:{}"),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=...,                 value=None),       True, id="Optional[dict|default:...|value:None"),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=None,                value={"x": "y"}), True, id="Optional[dict|default:None|value:{x:y}"),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=None,                value=...),        False, id="Optional[dict]|default:None|value:..."),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=None,                value={}),         True, id="Optional[dict]|default:None|value:{}"),
    pytest.param(object_factory(Optional[dict[str, str]], static_default=None,                value=None),       False, id="Optional[dict]|default:None|value:None"),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=dict,               value={"x": "y"}), True, id="Optional[dict]|default:{}|value:{x:y}"),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=dict,               value=...),        False, id="Optional[dict]|default:{}]|value:..."),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=dict,               value={}),         False, id="Optional[dict]|default:{}|value:{}"),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=dict,               value=None),       True, id="Optional[dict]|default:{}|value:None"),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=lambda: {"x": "y"}, value={"x": "y"}), True, id="Optional[dict]|default:{x:y}|value:{x:y}"),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=lambda: {"x": "y"}, value=...),        True, id="Optional[dict]|default:{x:y}|value:..."),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=lambda: {"x": "y"}, value={}),         True, id="Optional[dict]|default:{x:y}|value:{}"),
    pytest.param(object_factory(Optional[dict[str, str]], default_factory=lambda: {"x": "y"}, value=None),       True, id="Optional[dict]|default:{x:y}|value:None"),
    # Object cases...
    pytest.param(object_factory(Obj,           static_default=...,               value=Obj(n=0)), True, id="Obj|default:...|value:Obj(n=0)"),
    pytest.param(object_factory(Obj,           static_default=...,               value=Obj()),    True, id="Obj|default:...|value:Obj"),
    pytest.param(object_factory(Obj,           default_factory=Obj,              value=Obj(n=0)), True, id="Obj|default:Obj|value:Obj(n=0)"),
    pytest.param(object_factory(Obj,           default_factory=Obj,              value=...),      False, id="Obj|default:Obj]|value:..."),
    pytest.param(object_factory(Obj,           default_factory=Obj,              value=Obj()),    False, id="Obj|default:Obj|value:Obj"),
    pytest.param(object_factory(Obj,           default_factory=lambda: Obj(n=0), value=Obj(n=0)), True, id="Obj|default:Obj(n=0)|value:Obj(n=0)"),
    pytest.param(object_factory(Obj,           default_factory=lambda: Obj(n=0), value=...),      True, id="Obj|default:Obj(n=0)|value:..."),
    pytest.param(object_factory(Obj,           default_factory=lambda: Obj(n=0), value=Obj()),    True, id="Obj|default:Obj(n=0)|value:Obj"),
    pytest.param(object_factory(Optional[Obj], static_default=...,               value=Obj(n=0)), True, id="Optional[Obj|default:...|value:Obj(n=0)"),
    pytest.param(object_factory(Optional[Obj], static_default=...,               value=Obj()),    True, id="Optional[Obj|default:...|value:Obj"),
    pytest.param(object_factory(Optional[Obj], static_default=...,               value=None),     True, id="Optional[Obj|default:...|value:None"),
    pytest.param(object_factory(Optional[Obj], static_default=None,              value=Obj(n=0)), True, id="Optional[Obj|default:None|value:Obj(n=0)"),
    pytest.param(object_factory(Optional[Obj], static_default=None,              value=...),      False, id="Optional[Obj|default:None]|value:..."),
    pytest.param(object_factory(Optional[Obj], static_default=None,              value=Obj()),    True, id="Optional[Obj|default:None|value:Obj"),
    pytest.param(object_factory(Optional[Obj], static_default=None,              value=None),     False, id="Optional[Obj|default:None|value:None"),
    pytest.param(object_factory(Optional[Obj], default_factory=Obj,              value=Obj(n=0)), True, id="Optional[Obj|default:Obj|value:Obj(n=0)"),
    pytest.param(object_factory(Optional[Obj], default_factory=Obj,              value=...),      False, id="Optional[Obj|default:Obj]|value:..."),
    pytest.param(object_factory(Optional[Obj], default_factory=Obj,              value=Obj()),    False, id="Optional[Obj|default:Obj|value:Obj"),
    pytest.param(object_factory(Optional[Obj], default_factory=Obj,              value=None),     True, id="Optional[Obj|default:Obj|value:None"),
    pytest.param(object_factory(Optional[Obj], default_factory=lambda: Obj(n=0), value=Obj(n=0)), True, id="Optional[Obj|default:Obj(n=0)|value:Obj(n=0)"),
    pytest.param(object_factory(Optional[Obj], default_factory=lambda: Obj(n=0), value=...),      True, id="Optional[Obj|default:Obj(n=0)|value:..."),
    pytest.param(object_factory(Optional[Obj], default_factory=lambda: Obj(n=0), value=Obj()),    True, id="Optional[Obj|default:Obj(n=0)|value:Obj"),
    pytest.param(object_factory(Optional[Obj], default_factory=lambda: Obj(n=0), value=None),     True, id="Optional[Obj|default:Obj(n=0)|value:None"),
)
# fmt: on


@pytest.mark.parametrize(("obj", "expect_field"), FIELD_CASES)
def test_exclude_default_nulls_and_empty(obj, expect_field):
    serialised = obj.model_dump()
    if expect_field:
        assert FIELD_NAME in serialised
    else:
        assert FIELD_NAME not in serialised
