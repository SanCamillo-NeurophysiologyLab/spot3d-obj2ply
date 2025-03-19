import argparse
import sys
from pathlib import Path

from art import tprint

import pymeshlab 

# The pipeline to convert from .obj to colorized .ply comes directly from https://gist.github.com/SeungBack/e71eac0faa52088e3038395fef684494

def load_obj(file, verbosity=False):
    # load a mesh file (e.g. a .obj)
    ms = pymeshlab.MeshSet()
    ms.set_verbosity(verbosity)
    ms.load_new_mesh(str(file))
    return ms

def scale_m2mm(ms):
    # scale a mesh from meters to millimeters
    factor = 1000
    ms.compute_matrix_from_scaling_or_normalization(axisx = factor, axisy = factor, axisz = factor)
    return ms

def rotate(ms):
    # rotate the mesh to put the face on the correct orientation
    ms.compute_matrix_from_rotation(angle = 90.000000)
    return ms

def centralize(ms):
    # centralize the mesh
    ms.compute_matrix_from_translation(traslmethod = 2)
    return ms

def subdivide(ms):
    # subdivide the mesh
    # ms.meshing_surface_subdivision_midpoint(iterations = 100)
    ms.meshing_surface_subdivision_catmull_clark()
    ms.meshing_surface_subdivision_catmull_clark()
    return ms

def colorize(ms):
    # colorize vertices using uv texture
    ms.compute_color_from_texture_per_vertex()
    return ms

def triangularize(ms):
    ms.meshing_poly_to_tri()
    return ms

def export(ms, outfile):
    ms.save_current_mesh(
        file_name=str(outfile),
        binary=False,
        save_textures=False,
        save_vertex_quality=False,
        save_vertex_color=True,
        save_vertex_normal=True,
        save_vertex_flag=False,
        save_vertex_coord=False,
        save_vertex_radius=False,
        save_face_flag=False,
        save_face_color=False,
        save_wedge_color=False,
        save_wedge_texcoord=False,
        save_wedge_normal=False

    )

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser(
        description="Convert .obj file (scaled in m) to colorized .ply (scaled in mm). Compatible with Spot3D."
    )
    parser.add_argument(
        "input",
        help="the input .obj file"    
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="",
        help="the output .ply file. Default input.ply"    
    )

    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="force to overwrite the output"    
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="set verbose output"    
    )

    tprint("SPOT3D")
    tprint(".obj 2 .ply")

    # Pars and validate arguments
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    # Check input
    if not args.input:
        parser.exit(1, message=f"You have to specify a .obj file\n")

    input_obj = Path(args.input)
    
    if not input_obj.exists():
        parser.exit(1, f"The file {input_obj} does not exist\n")

    if not input_obj.suffix == ".obj":
        parser.exit(1, f"The file {input_obj} is not a .obj file\n")
    
    # Check output
    if not args.output:
        output_ply = input_obj.with_suffix(".ply")
    else:
        output_ply = Path(args.output)
        if output_ply.is_dir:
            output_ply = output_ply / input_obj.with_suffix(".ply").name
    
    if output_ply.exists() and not args.force:
        parser.exit(1, f"The output file {output_ply} already exists! If you want to overwrite add the --force flag to the command\n")
    elif output_ply.exists():
        print(f"[WARNING] You are overwriting the file {output_ply}")

    if not output_ply.suffix == ".ply":
        parser.exit(1, f"The output file {output_ply} is not a .ply file\n")

    # Create output folder
    output_ply.parent.mkdir(parents=True, exist_ok=True)

    # Run the whole pipeline
    
    ms = load_obj(input_obj, verbosity=args.verbose)
    ms = scale_m2mm(ms)
    ms = rotate(ms)
    ms = centralize(ms)
    ms = subdivide(ms)
    ms = colorize(ms)
    ms = triangularize(ms)
    export(ms, output_ply)

    print(f"\nFINISH!\nThe converted file is saved here: {output_ply}")