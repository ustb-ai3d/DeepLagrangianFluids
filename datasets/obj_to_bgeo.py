import os
import open3d as o3d
import numpy as np
from datasets.create_physics_scenes import obj_surface_to_particles, write_bgeo_from_numpy

def obj_to_bgeo(bb_obj, box_output_path, translation=None, scale=None):
    # convert bounding box to particles
    bb, bb_normals = obj_surface_to_particles(bb_obj, radius=0.01)
    if scale:
        bb *= scale
    if translation:
        bb += translation
    write_bgeo_from_numpy(box_output_path, bb, bb_normals)

if __name__ == '__main__':
    # select random bounding box
    bb_obj = r'/workdir/fluidmlp3/data/test_scenes/03/bgeo/cupobj.obj'
    translation = [0, 2, 0]
    scale = [4.0, 4.0, 1.5]
    # bounding box
    box_output_path = os.path.join('/workdir/fluidmlp3/data/test_scenes/03/bgeo/box.bgeo')
    obj_to_bgeo(bb_obj, box_output_path)
    # obj_to_bgeo(bb_obj, box_output_path, translation, scale)