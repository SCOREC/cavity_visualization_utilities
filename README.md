# Cavity Visulization Utilities

The tools in this repo can be used along with the utility [makeAllCavities.cc](https://github.com/SCOREC/core/blob/master/test/makeAllCavities.cc) in the [SCOREC/Core](https://github.com/SCOREC/core) repo, to visualize curved cavities during mesh adaptation. A short description of how these tools can be used are provided below.

j## Generationg the Cavities

To generate the cavities you will need an installation of [SCOREC/Core](https://github.com/SCOREC/core) with the following `CMAKE` option `-DBUILD_EXES=ON`. Then you can generate cavities associated with a mehs by calling 

```
paht_to/make_all_cavities <model> <mesh> <prefix> <res> <mode>
```
where

* `model`  is the path to the model file
* `mesh`   is the path to the mesh file
* `prefix` is the path to the root directory to save the cavities
* `res`    is the resolution used to write curved vtk files
* `mode`   is specifies the cavities that are being created/outputted to vtk


The `mode` s have to be selected from the following list


* `aa`  creates all vert, edge, and face cavities
* `ai`  creates all vert, edge, and face cavities classified on a model region
* `ab`  creates all vert, edge, and face cavities classified on model boundary
* `va`  creates all vert cavities
* `vi`  creates all vert cavities classified on a model region
* `vb`  creates all vert cavities classified on model boundary
* `ea`  creates all edge cavities
* `ei`  creates all edge cavities classified on a model region
* `eb`  creates all edge cavities classified on model boundary
* `fa`  creates all face cavities
* `fi`  creates all face cavities classified on a model region
* `fb`  creates all face cavities classified on model boundary
* `ls`  prompts user to provide a list of entities and creates only those cavities
* `tagname` looks for a tag with name __tagname__ on the mesh and create cavities for all the entities that return true for `m->hasTag(e, t)`.


The output of above call would be stored under a directory named `prefix` with the following folder structure:

```
 prefix
 ├── cavities
 │ ├── edge_nnnnn
 │ ├── vertex_nnnnn
 │ └── triangle_nnnnn
 └── mesh
```

where the subdirectory `cavities` contains all the cavites created by the utility and `mesh` contains the original mesh (depending on the situation these subfolders may contian smb and vtk files for the curved cavity and the curved cavity wireframe, the corresponding linear cavity and the entity itself)

# Visualizing the Cavities

The cavities generated above can be visualized using `pvpython` (provided by `ParaView`) and the script `python/show_curved_cavity.py` as follows

```
pvpython path_to/show_curved_cavity.py [-h] -r ROOT_DIR -c CAVITY_NAME [-p] [-m]
```

where the arguments are as follows


* `-r, --root_dir`     path to the root directory containing the cavities [required]
* `-c, --cavity_name`  the name of the cavity of interest [required]
* `-p, --save_png`     if given saves the png of the RenderView
* `-m, --show_mesh`    if given shows the entire mesh (with low opacity) along with the cavity in RenderView


For example to visualize the cavity `edge_00092` in the example folder of this repo one can call any of the following:

```
pvpython path_to/show_curved_cavity.py -r path_to/examples/cubic_slab_cubic_slab_cavities -c edge_00092
pvpython path_to/show_curved_cavity.py -r path_to/examples/cubic_slab_cubic_slab_cavities -c edge_00092 -m
pvpython path_to/show_curved_cavity.py -r path_to/examples/cubic_slab_cubic_slab_cavities -c edge_00092 -m -c
```

The first one only shows the cavity in the RenderView, the second one shows the cavity and the whole mesh in the RenderView, and the last one shows both the cavity and the mesh in the RenderView and saves a png with name `edge_00092.png` of the RenderView before any interactions (i.e., before any rotation or translation of the Camera by the user).

Example pngs created for `edge_00092` and `vertex_00026` are as follwos
![example_pic](https://user-images.githubusercontent.com/1325140/165379629-97b7ab34-6f34-4e4b-860e-09ff45d91ac7.png)

