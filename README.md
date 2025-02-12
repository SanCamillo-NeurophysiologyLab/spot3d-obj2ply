# SPOT3D - .obj 2 .ply

This simple scripts converts a file .obj acquired with the new Structure Sensor 3 to a file .ply compatible with Spot3D (i.e. colorized vertices and scale in mm).

## Usage

Create a python environment and install the requirements
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the script (from the activated environment)
```bash
python obj2ply.py input.obj output.ply
```

`output.ply` is an optional arguments. If it is missing the output will be `input.ply`. 

If you want to overwrite the output file add the flag `-f` (or the equivalent `--force`).

The usage is simple, but you can find a reminder of that in the help

```
>>> python obj2ply.py -h
 ____   ____    ___   _____  _____  ____  
/ ___| |  _ \  / _ \ |_   _||___ / |  _ \ 
\___ \ | |_) || | | |  | |    |_ \ | | | |
 ___) ||  __/ | |_| |  | |   ___) || |_| |
|____/ |_|     \___/   |_|  |____/ |____/ 
                                          

           _        _   ____              _        
     ___  | |__    (_) |___ \      _ __  | | _   _ 
    / _ \ | '_ \   | |   __) |    | '_ \ | || | | |
 _ | (_) || |_) |  | |  / __/   _ | |_) || || |_| |
(_) \___/ |_.__/  _/ | |_____| (_)| .__/ |_| \__, |
                 |__/             |_|        |___/ 

usage: obj2ply.py [-h] [-f] [-v] input [output]

Convert obj file to colorized ply scaled in mm. Compatible with Spot3D.

positional arguments:
  input          the input .obj file
  output         the output .ply file. Default input.ply

optional arguments:
  -h, --help     show this help message and exit
  -f, --force    force to overwrite the output
  -v, --verbose  set verbose output
```

## Credits

It is a simple python script which uses the [pymeshlab](pymeshlab.readthedocs.io) library.
The script is an adaptation of the very useful instruction on [how to convert a .obj to .ply in meshlab](https://gist.github.com/SeungBack/e71eac0faa52088e3038395fef684494).

## Pipeline

1. Load the .obj
2. Scale the mesh from m to mm
3. Centralize the mesh
4. Subdivide the mesh
5. Colorize the vertices
6. Triangularize faces
7. Export the .ply