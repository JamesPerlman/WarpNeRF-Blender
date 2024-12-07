from typing import Tuple
import bpy
import math
import numpy as np

def bl_get_camera_sensor_size_in_pixels(
    camera_data: bpy.types.Camera,
    wn_cam_dims: Tuple[int, int]
) -> Tuple[float, float]:

    nerf_w, nerf_h = wn_cam_dims
    bl_sw = camera_data.sensor_width
    bl_sh = camera_data.sensor_height

    px_w: float
    px_h: float
    
    if camera_data.sensor_fit == 'AUTO':
        bl_asp = 1.0
        nerf_asp = nerf_h / nerf_w

        if nerf_asp > bl_asp:
            px_w = nerf_h / bl_asp
            px_h = nerf_h
        else:
            px_w = nerf_w
            px_h = nerf_w * bl_asp

    elif camera_data.sensor_fit == 'HORIZONTAL':
        px_w = nerf_w
        px_h = nerf_w * bl_sh / bl_sw

    elif camera_data.sensor_fit == 'VERTICAL':
        px_w = nerf_h * bl_sw / bl_sh
        px_h = nerf_h

    return px_w, px_h

def bl2wn_camera_focal_length(
    camera_data: bpy.types.Camera,
    wn_cam_dims: Tuple[int, int]
) -> float:

    bl_sw = camera_data.sensor_width
    bl_f  = camera_data.lens
    px_w, px_h = bl_get_camera_sensor_size_in_pixels(camera_data, wn_cam_dims)
    
    # focal length in pixels
    return bl_f / bl_sw * px_w

def wn2bl_camera_focal_length(
    camera_data: bpy.types.Object,
    wn_cam_dims: Tuple[int, int],
    wn_focal_length: float
) -> float:
    
    bl_sw = camera_data.sensor_width
    px_w, px_h = bl_get_camera_sensor_size_in_pixels(camera_data, wn_cam_dims)
    
    # focal length in mm
    return wn_focal_length * bl_sw / px_w

def get_camera_shift(
    context: bpy.types.Context,
    camera_obj: bpy.types.Object,
    fl_x: float,
    img_dims: Tuple[int, int]
) -> Tuple[float, float]:
    
    cam_data: bpy.types.Camera = camera_obj.data
    render: bpy.types.RenderSettings = context.scene.render
    out_res_x = render.resolution_x
    out_res_y = render.resolution_y
    cam_fl = bl2wn_camera_focal_length(camera_obj, (out_res_x, out_res_y))

    cam_angle_x = 2.0 * math.atan2(0.5 * out_res_x, cam_fl)
    
    cam_res_x = 2.0 * fl_x * math.tan(0.5 * cam_angle_x)
    cam_res_y = out_res_y / out_res_x * cam_res_x

    horizontal_fit = cam_data.sensor_fit == 'HORIZONTAL' or (cam_data.sensor_fit == 'AUTO' and cam_res_x > cam_res_y)

    if horizontal_fit:
        u = cam_res_x / img_dims[0]
        v = cam_res_x / img_dims[1]
    else:
        u = cam_res_y / img_dims[0]
        v = cam_res_y / img_dims[1]
    
    return u * cam_data.shift_x, v * cam_data.shift_y
