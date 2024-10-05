# Maryam Rezaee (ms.maryamrezaee@gmail.com)

import sympy as sp
import numpy as np


def canApply(A):
    n = A.shape[0]
    return np.linalg.matrix_rank(A) == n


def upTriangular(aug_matrix):

    for row in range(0, aug_matrix.shape[0]):

        swap_iter = 1
        pivot = aug_matrix[row][row]

        # swap rows if pivot = 0
        while pivot == 0 and row + swap_iter < aug_matrix.shape[0]:
            
            aug_matrix[[row, 
                        row + swap_iter]] = aug_matrix[[row + swap_iter,
                                                         row]]
            swap_iter += 1
            pivot = aug_matrix[row][row]

        # if pivot = 0 still, remaining rows are all zeros
        if pivot == 0:
            return aug_matrix

        # else pivot != 0, continue with method
        curr_row = aug_matrix[row]
        aug_matrix[row] = curr_row / pivot

        for swap_iter in range(row + 1, aug_matrix.shape[0]):
            aug_matrix[swap_iter] = aug_matrix[swap_iter] - aug_matrix[row] * aug_matrix[swap_iter][row]

    return aug_matrix


def backSubstitution(up_tri_matrix):

    n = up_tri_matrix.shape[0]
    syms = list(sp.symbols('x0:%d'%n))

    for i, row in reversed(list(enumerate(up_tri_matrix))):
        eqn = -up_tri_matrix[i][-1]
        
        for j in range(len(syms)):
            eqn += syms[j] * row[j]

        syms[i] = sp.solve(eqn, syms[i])[0]

    return syms


def solve(A, b):

    aug_matrix = np.column_stack((A, b))
    
    up_tri_matrix = upTriangular(aug_matrix)
    nozero_matrix = up_tri_matrix[~np.isclose(up_tri_matrix, 0).all(axis=1)]
    solution = backSubstitution(nozero_matrix)

    return solution


'''
if __name__ == "__main__":

    Abase = [[ 1, -2, -1],
         [ 2,  2, -1.],
         [-1, -1,  2,]]
    A = np.asarray(Abase)
    bbase = [6, 1, 1]
    b = np.asarray(bbase)

    print(solve(A, b))

    A = np.random.rand(10, 10)
    b = np.random.rand(10)

    print(solve(A, b))
'''