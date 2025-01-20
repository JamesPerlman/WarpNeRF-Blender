__reload_order_index__ = -1

import bpy
from warpnerf.scene.object_identifiers import (
    WN_OBJ_ATTR_PREFIX,
    WN_OBJECT_ID,
    WN_OTYPE_IDENTIFIER,
    WN_OTYPE_RADIANCE_FIELD
)

def is_warpnerf_obj(obj: bpy.types.Object) -> bool:
    return WN_OTYPE_IDENTIFIER in obj and WN_OBJECT_ID in obj

def get_obj_type(obj: bpy.types.Object) -> str | None:
    if is_warpnerf_obj(obj):
        return obj[WN_OTYPE_IDENTIFIER]
    else:
        return None

def set_obj_type(obj: bpy.types.Object, obj_type: str):
    obj[WN_OTYPE_IDENTIFIER] = obj_type

def is_obj_type(obj: bpy.types.Object, obj_type: str) -> bool:
    return get_obj_type(obj) == obj_type

def get_closest_parent_of_type(obj: bpy.types.Object, obj_type: str) -> bpy.types.Object | None:
    target = obj
    while target is not None:
        if is_obj_type(target, obj_type):
            return target
        target = target.parent
    return None

def is_self_or_some_parent_of_type(obj: bpy.types.Object, obj_type: str) -> bool:
    return get_closest_parent_of_type(obj, obj_type) is not None

def get_first_child_of_type(obj: bpy.types.Object, obj_type: str) -> bpy.types.Object | None:
    for child in obj.children:
        if is_obj_type(child, obj_type):
            return child

    for child in obj.children:
        target = get_first_child_of_type(child, obj_type)
        if target is not None:
            return target

    return None

def get_active_obj_of_type(context, type: str) -> bpy.types.Object | None:
    active_obj = context.active_object
    obj = get_closest_parent_of_type(active_obj, type)
    return obj

def get_active_nerf_obj(context) -> bpy.types.Object | None:
    return get_active_obj_of_type(context, WN_OTYPE_RADIANCE_FIELD)

def get_obj_id(obj: bpy.types.Object) -> int | None:
    if is_warpnerf_obj(obj):
        return obj[WN_OBJECT_ID]
    else:
        return None

def set_obj_id(obj: bpy.types.Object, id: int):
    obj[WN_OBJECT_ID] = id

def get_obj_by_id(context, id: int, type: str = None) -> bpy.types.Object | None:
    for obj in context.scene.objects:
        if get_obj_id(obj) == id:
            if type is None:
                return obj
            if is_obj_type(obj, type):
                return obj
    return None

def get_obj_attr(obj: bpy.types.Object, attr_name: str):
    return obj.get(f'${WN_OBJ_ATTR_PREFIX}_${attr_name}')

def set_obj_attr(obj: bpy.types.Object, attr_name: str, value):
    obj[f'${WN_OBJ_ATTR_PREFIX}_${attr_name}'] = value