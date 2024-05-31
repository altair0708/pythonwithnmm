# Numerical Manifold Method (NMM)

## Introduction and Goals
3D NMM is a numerical calculation program to solve Partial Difference Equation(PDE). The main goal to develop
this program is to develop three-dimensional NMM, and for ***my doctor dissertation***.  
The process of NMM can be summarized as:
1. Preprocess
    - Establishment the geometric model (solvation domain).
    - Generate mathematics covers.
    - Generate physical covers (divide by solvation domain and mathematics covers).
    - Generate manifold elements (divide by physical covers).
    - Define material parameters.
2. Calculation
    - Loading boundary condition.
    - Calculation manifold element matrices.
    - Assemble total matrix.
    - Iterative solvation.
    - Refresh the physical covers, refresh and interpolate manifold elements.
    - Modify the status of manifold elements(such as geometric and topological information).
3. Postprocess
    - Output model status ever step.
    - Display contour of model. 
4. *Extension option*
    - *High performance computing*

## Solution Strategy
   - Python (Basic program language)
   - Visual ToolKit (VTK, Geometric calculation, Data structure and saving)
   - Gmsh (Preprocess)
   - Paraview (Postprocess)
   - Numpy and Scipy (Linear equations)
   - Json (Config file)
   - *OpenCascade (OCC, Geometric calculation)*

## Building Block View
### preprocess

