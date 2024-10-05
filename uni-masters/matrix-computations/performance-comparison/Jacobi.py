# Maryam Rezaee (ms.maryamrezaee@gmail.com)

import numpy as np


def canApply(A):

    D = np.diag(np.diag(A))
    L = np.tril(A) - D
    U = np.triu(A) - D
    
    J_matrix = -1 * np.linalg.inv(D) @ (L + U)

    eigenvalues = np.linalg.eigvals(J_matrix)
    max_eigenvalue = np.max(np.abs(eigenvalues))

    if max_eigenvalue < 1:
        return True
    else:
        return False


def canApplyEstimate(A):

    D = np.diag(A)  
    if np.any(D == 0):
        return False
    
    Jacobi_matrix_norm = np.linalg.norm(np.diag(1/D) @ (D - A))
    if Jacobi_matrix_norm >= 1:
        return False
    
    return True


# COMMENTS FOR FUTURE OPTIMIZATION:
# change calculation from item iteartion to matrix formula
# create random vector for initial guess
def solve(A, b, x0=None, epsilon=1e-6, max_iterations=100):

    n = A.shape[0]
    
    x0 = np.zeros(n) if x0 is None else np.array(x0)
    x = x0.copy()
    
    for iter in range(max_iterations):

        x_prev = x.copy()
        for i in range(n):
            sum_term = np.dot(A[i], x_prev) - A[i, i] * x_prev[i]
            x[i] = (b[i] - sum_term) / A[i, i]
        
        error = np.linalg.norm(x - x_prev)
        if error < epsilon:
            return x
    
    return x

'''
if __name__ == "__main__":

    A = np.array([[2.0,1.0],[5.0,7.0]])
    b = np.array([11.0,13.0])
    guess = np.array([1.0,1.0])

    print(canApply(A))
    print(solve(A, b, x0 = guess))

    A = np.random.rand(10, 10)
    b = np.random.rand(10)

    print(canApply(A))
    print(solve(A, b))
'''