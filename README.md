# Computational Topology


These are some projects from a computational topology course given in Spring 2020. The projects based on  Herbert Edelsbrunner and J Harer's [Computational Topology : An Introduction](https://www.maths.ed.ac.uk/~v1ranick/papers/edelcomp.pdf)

The three main components of the code:

## Triangulation

Triangulation.py is a data structure to represent a triangulation. It takes triangles as input and forms them into a graph that represents the triangulation. The code determines the manifold's Euler characteristic, genus, and specific name of the manifold if it has one. 

## Simplicial Complex & Boundary Matrix
SimplicialComplex.py takes a simplex as input and forms it into a multi-dimensional simplicial complex. The code then calculates the boundary matrix for each dimension of the complex. 

## Persistent Homology

PersistentHomology.py is an algorithm to compute the persistent homology of a manifold from its boundary matrix. 
