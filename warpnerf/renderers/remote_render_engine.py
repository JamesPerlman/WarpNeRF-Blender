from typing import Tuple
import bpy
import array
import threading
import time
import random

from gpu_extras.presets import draw_texture_2d

from warpnerf.networking.requests.render_request import RenderRequest
from warpnerf.networking.warpnerf_client import WarpNeRFClient
from warpnerf.scene.objects.perspective_camera import PerspectiveCamera
from warpnerf.scene.objects.wn_scene import WNScene

class RemoteRenderEngine(bpy.types.RenderEngine):
    bl_idname = "WARPNERF_REMOTE_RENDER_ENGINE"
    bl_label = "WarpNeRF (Remote)"
    bl_use_preview = True

    def __init__(self):
        self.scene_data = None
        self.draw_data = None
        # Threading status
        self.long_render_thread = None
        self.long_render_finished = False
        self.long_render_pixels = None
        self.prev_camera: PerspectiveCamera = None
        self.prev_dims: Tuple[int, int] = None
        self.subscriptions = []
        self.client = WarpNeRFClient()

        self.register_callbacks()

    def __del__(self):
        self.unregister_callbacks()

    def register_callbacks(self):
        self.unregister_callbacks()
        self.subscriptions.append(
            WarpNeRFClient().subscribe("render_result", self._on_render_result)
        )
    
    def unregister_callbacks(self):
        for unsubscribe in self.subscriptions:
            unsubscribe()
        self.subscriptions = []
    
    ######################
    # Remote renderer hooks
    def _on_render_result(self, data):
        print("----------------")
        print("RECEIVED RENDER RESULT")
        print(data)
        print("----------------")

    ######################
    # RenderEngine methods

    def render(self, depsgraph):
        """
        F12 render. We'll just do a simple color fill.
        """
        scene = depsgraph.scene
        scale = scene.render.resolution_percentage / 100.0
        self.size_x = int(scene.render.resolution_x * scale)
        self.size_y = int(scene.render.resolution_y * scale)

        # Fill the render result with a flat color
        if self.is_preview:
            color = [0.1, 0.2, 0.1, 1.0]
        else:
            color = [0.2, 0.1, 0.1, 1.0]

        pixel_count = self.size_x * self.size_y
        rect = [color] * pixel_count

        result = self.begin_result(0, 0, self.size_x, self.size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = rect
        self.end_result(result)

    def view_update(self, context, depsgraph):
        """
        Called whenever the scene or 3D viewport changes.
        """

        print("view_update")
        region = context.region
        scene = depsgraph.scene

        # If we haven't set up scene_data, do so now
        if not self.scene_data:
            self.scene_data = []
            for datablock in depsgraph.ids:
                pass  # no-op
        else:
            for update in depsgraph.updates:
                print("Datablock updated: ", update.id.name)
            if depsgraph.id_type_updated('MATERIAL'):
                print("Materials updated")

    def view_draw(self, context, depsgraph):
        """
        Called every time the 3D viewport is drawn. 
        """

        # Create a Camera object from the current 3D viewport

        current_region3d: bpy.types.RegionView3D = None
        for area in context.screen.areas:
            area: bpy.types.Area
            if area.type == 'VIEW_3D':
                current_region3d = area.spaces.active.region_3d
        
        if current_region3d is None:
            return

        camera = PerspectiveCamera.from_blender(context, current_region3d)

        print("view_draw")
        import gpu

        region = context.region
        scene = depsgraph.scene
        dimensions = (region.width, region.height)

        is_user_initiated = (camera != self.prev_camera) or (dimensions != self.prev_dims)

        # Bind display shader
        gpu.state.blend_set('ALPHA_PREMULT')
        self.bind_display_space_shader(scene)

        # Create or resize the draw data
        if not self.draw_data or self.draw_data.dimensions != dimensions:
            self.draw_data = CustomDrawData(dimensions)

        # If final pixels are ready, show them; else the quick pass
        if self.long_render_finished and self.long_render_pixels is not None:
            print("Using final rendered image for drawing.")
            self.draw_data.update_texture(self.long_render_pixels)
        else:
            print("Using quick pass for drawing.")
        
        # If there's no thread running, start a new 1-second "long render"
        if is_user_initiated and (not self.long_render_thread or not self.long_render_thread.is_alive()):
         
            print("Submitting render request...")

            request = RenderRequest()
            request.scene = WNScene.from_blender(context, scene)
            request.camera = camera
            request.size = dimensions

            print(request.to_dict())

            self.long_render_finished = False
            self.long_render_pixels = None
            self.long_render_thread = threading.Thread(
                target=self._long_render_process,
                args=(dimensions,)
            )
            self.long_render_thread.start()

        # Draw the texture
        self.draw_data.draw()

        # Unbind
        self.unbind_display_space_shader()
        gpu.state.blend_set('NONE')

        self.prev_camera = camera
        self.prev_dims = dimensions

    def _long_render_process(self, dimensions):
        """
        Simulates a 1-second "heavy" render that produces random noise.
        """
        print("Long render started...")
        time.sleep(1.0)  # simulate remote or heavy-lift

        width, height = dimensions
        pixel_count = width * height

        # random noise, each pixel is [r, g, b, a].
        final_pixels = [
            [random.random(), random.random(), random.random(), 1.0]
            for _ in range(pixel_count)
        ]

        self.long_render_pixels = final_pixels
        self.long_render_finished = True
        print("Long render finished!")
        self.tag_redraw()

class CustomDrawData:
    def __init__(self, dimensions):
        """
        Create a quick-pass texture (solid color).
        """
        import gpu
        self.dimensions = dimensions
        width, height = dimensions

        # Quick color
        color = [0.1, 0.2, 0.1, 1.0]
        pixel_count = width * height
        pixels = color * pixel_count

        # Convert to GPU buffer
        pixels = gpu.types.Buffer('FLOAT', width * height * 4, pixels)
        self.texture = gpu.types.GPUTexture((width, height), format='RGBA16F', data=pixels)

    def __del__(self):
        del self.texture

    def update_texture(self, pixels):
        """
        Because some Blender versions don't support GPUTexture.update/write,
        we recreate the texture whenever we get new data.
        """
        import gpu
        width, height = self.dimensions

        # Flatten out the pixel data
        flat_pixels = []
        for rgba in pixels:
            flat_pixels.extend(rgba)

        buf = gpu.types.Buffer('FLOAT', width * height * 4, flat_pixels)

        # Destroy old texture
        del self.texture

        # Create a new texture with fresh data
        self.texture = gpu.types.GPUTexture((width, height), format='RGBA16F', data=buf)

    def draw(self):
        draw_texture_2d(self.texture, (0, 0), self.texture.width, self.texture.height)

def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
    }

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'WARPNERF_REMOTE_RENDER_ENGINE') and 'BLENDER_RENDER' in panel.COMPAT_ENGINES:
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels

def register_remote_render_engine():
    bpy.utils.register_class(RemoteRenderEngine)
    for panel in get_panels():
        panel.COMPAT_ENGINES.add('WARPNERF_REMOTE_RENDER_ENGINE')

def unregister_remote_render_engine():
    bpy.utils.unregister_class(RemoteRenderEngine)
    for panel in get_panels():
        if 'WARPNERF_REMOTE_RENDER_ENGINE' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('WARPNERF_REMOTE_RENDER_ENGINE')
