from dataclasses import is_dataclass, fields, asdict
from typing import TypeVar, Type, Dict, Any, get_origin, Union, get_args

from pydantic import BaseModel

T = TypeVar('T')


# ================== Utils to for dataclass <-> dict parsing ===========================
def dict_to_dataclass_or_basemodel(cls: Type[T], data: Dict[str, Any]) -> T:
    """Recursively converts a dictionary into a dataclass or BaseModel instance, handling nested and optional fields."""
    if is_dataclass(cls):
        init_kwargs = {}
        for field in fields(cls):
            field_name = field.name
            field_type = field.type
            field_value = data.get(field_name, None)  # Default to None if key is missing

            # Resolve Optional and Union types
            if get_origin(field_type) is Union:
                # Handle Optional (Union[X, None]) by extracting the actual type
                actual_types = get_args(field_type)
                if len(actual_types) == 2 and type(None) in actual_types:
                    actual_type = next(t for t in actual_types if t is not type(None))
                else:
                    actual_type = None
            else:
                actual_type = field_type

            # Check if the actual type is a dataclass or BaseModel
            if actual_type and isinstance(actual_type, type):
                if is_dataclass(actual_type):
                    init_kwargs[field_name] = dict_to_dataclass_or_basemodel(actual_type, field_value) if field_value else None
                elif issubclass(actual_type, BaseModel):
                    init_kwargs[field_name] = actual_type(**field_value) if field_value else None
                else:
                    init_kwargs[field_name] = field_value
            else:
                init_kwargs[field_name] = field_value

        return cls(**init_kwargs)
    elif issubclass(cls, BaseModel):
        return cls(**data)
    else:
        raise TypeError(f"{cls} is neither a dataclass nor a BaseModel.")


def convert_to_obj(data: Any) -> Any:
    if is_dataclass(data):
        return {k: convert_to_obj(v) for k, v in asdict(data).items()}
    elif isinstance(data, BaseModel):
        return {k: convert_to_obj(v) for k, v in data.dict().items()}
    elif isinstance(data, list):
        return [convert_to_obj(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_to_obj(v) for k, v in data.items()}
    return data

