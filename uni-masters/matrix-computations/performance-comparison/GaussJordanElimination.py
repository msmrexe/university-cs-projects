# Maryam Rezaee (ms.maryamrezaee@gmail.com)

import numpy as np


def canApply(A):
    n = A.shape[0]
    return np.linalg.matrix_rank(A) == n

     
def upTriangular(aug_matrix):
    
    n = aug_matrix.shape[0]
    for i in range(n):
        if aug_matrix[i, i] == 0:
            # find a non-zero pivot element below the current row
            for k in range(i + 1, n):
                if aug_matrix[k, i] != 0:
                    aug_matrix[[i, k]] = aug_matrix[[k, i]]
                    break

        pivot = aug_matrix[i, i]

        # divide the pivot row by the pivot element
        curr_row = aug_matrix[i, :]
        aug_matrix[i, :] = curr_row / pivot

        # eliminate non-zero elements below the pivot
        for j in range(i + 1, n):
            if aug_matrix[j, i] != 0:
                factor = aug_matrix[j, i]
                aug_matrix[j, :] -= factor * aug_matrix[i, :]
                
    return aug_matrix


def backSubstitution(up_tri_matrix):

    n = up_tri_matrix.shape[0]
    
    for i in range(n - 1, 0, -1):
        for j in range(i - 1, -1, -1):
            if up_tri_matrix[j, i] != 0:
                factor = up_tri_matrix[j, i]
                up_tri_matrix[j, :] -= factor * up_tri_matrix[i, :]
                
    return up_tri_matrix
                

def solve(A, b):
    
    aug_matrix = np.column_stack((A, b))

    up_tri_matrix = upTriangular(aug_matrix)
    uni_diag = backSubstitution(up_tri_matrix)
    solution = uni_diag[:, -1]
    
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