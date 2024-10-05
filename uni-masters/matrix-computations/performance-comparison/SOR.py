# Maryam Rezaee (ms.maryamrezaee@gmail.com)

import numpy as np


def canApply(A, omega):

    D = np.diag(np.diag(A))
    L = np.tril(A) - D
    U = np.triu(A) - D

    SOR_matrix = np.linalg.inv(D + omega * L) @ (-1 * omega * U + (1 - omega) * D)
    
    eigenvalues = np.linalg.eigvals(SOR_matrix)
    max_eigenvalue = np.max(np.abs(eigenvalues))

    if max_eigenvalue < 1:
        return True
    else:
        return False

# COMMENTS FOR FUTURE OPTIMIZATION:
# change calculation from item iteartion to matrix formula
# get initial guess from Jacobi
# choose random omega in (1,2)
def solve(A, b, omega=1.5, x0=None, epsilon=1e-6, max_iterations=100):
    
    n = A.shape[0]

    x = np.zeros(n) if x0 is None else np.array(x0) 
    residuals = [] 

    for iter in range(max_iterations):
        
        x_new = np.copy(x)
        for i in range(n):
            x_new[i] = (1 - omega) * x_new[i] + (omega / A[i, i]) * (b[i] - np.dot(A[i, :i], x_new[:i]) - np.dot(A[i, i + 1:], x[i + 1:]))
        
        residuals.append(np.linalg.norm(A @ x_new - b))
        
        error = np.linalg.norm(x_new - x)
        if error < epsilon:
            return x_new
        
        x = np.copy(x_new)

    return x_new

'''
if __name__ == "__main__":

    A = np.array([[10, -2, 1], [-1, 5, 1], [2, 3, 10]])
    b = np.array([7, -8, 6])

    solution = solve(A, b, omega=0.5, x0=None, epsilon=1e-8, max_iterations=100)

    print(canApply(A, 0.5))
    print(solution)

    A = np.random.rand(10, 10)
    b = np.random.rand(10)

    print(canApply(A, 1.5))
    print(solve(A, b))
'''