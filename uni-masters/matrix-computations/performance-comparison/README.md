# Project Overview

This project was defined as an additional final project for the Master's course of Matrix Computations (4021) at Sharif University of Technology. The code was implemented using Python programming language but with minimal usage of predefined Python functions and libraries. To import other modules and run all other files, open "Performance Comparison.py"

## Topic

Implementation of Iterative Methods for Solving Ax = b

## Description

Five comparable methods were selected and implemented as modules, including:

- Gaussian Elimination
- Gauss-Jordan Elimination
- Jacobi
- Gauss-Seidel
- SOR

In the main file "Performance Comparison," each module is tested on random matrices of increasing dimensions to measure the method's performance; for each test, the feasibility and solution accuracy is evluated to decide whether to run the method or produce a new matrix with the same dimensions. The final measurements are plotted as a graph to increase the ease of comparison.

### Note

The code is not optimized for high-dimensional matrices. Further research revealed that optimal calculations are generally performed using matrix equivalent formulas rather than manual iterative methods. I made a note to revisit and optimize the code in the future.
