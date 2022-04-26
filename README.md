# Cavity Visulization Utilities

The tools in this repo can be used along with the utility [makeAllCavities.cc](https://github.com/SCOREC/core/blob/master/test/makeAllCavities.cc) in the [SCOREC/Core](https://github.com/SCOREC/core) repo, to visualize curved cavities during mesh adaptation. A short description of how these tools can be used are provided below.

## Generationg the Cavities

To generate the cavities you will need an installation of [SCOREC/Core](https://github.com/SCOREC/core) with the following `CMAKE` option `-DBUILD_EXES=ON`. Then you can generate cavities associated with a mehs by calling 

```
paht_to/make_all_cavities <model> <mesh> <prefix> <resolution> <mode>
```
where

* `model` is the path to the model file

```
USAGE: ./test/make_all_cavities <model> <mesh> <prefix> <resolution> <mode>
modes are as follows 
aa: creates all vert, edge, face cavities
ai: creates all vert, edge, face cavities classified on interior
ab: creates all vert, edge, face cavities classified on boundary
va: creates all vert cavities
vi: creates all vert cavities classified on interior
vb: creates all vert cavities classified on boundary
ea: creates all edge cavities
ei: creates all edge cavities classified on interior
eb: creates all edge cavities classified on boundary
fa: creates all face cavities
fi: creates all face cavities classified on interior
fb: creates all face cavities classified on boundary
ls: get a list from user and creates cavities for that list
tagname: creates cavities for all entities that have tagname
```

# Visualizing the Cavities
