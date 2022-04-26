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
 │  ├── vertex_nnnnn
 │  └── triangle_nnnnn
 └── mesh
```

# Visualizing the Cavities
