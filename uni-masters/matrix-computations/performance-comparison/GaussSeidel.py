# Maryam Rezaee (ms.maryamrezaee@gmail.com)

import numpy as np


def canApply(A):

    D = np.diag(np.diag(A))
    L = np.tril(A) - D
    U = np.triu(A) - D
    
    GS_matrix = -1 * np.linalg.inv(L + D) @ U
    
    eigenvalues = np.linalg.eigvals(GS_matrix)
    max_eigenvalue = np.max(np.abs(eigenvalues))
    
    if max_eigenvalue < 1:
        return True
    else:
        return False

# COMMENTS FOR FUTURE OPTIMIZATION:
# change calculation from item iteartion to matrix formula
# get initial guess from Jacobi
def solve(A, b, x0=None, epsilon=1e-6, max_iterations=100):
    
    n = A.shape[0]
    
    x = np.zeros(n) if x0 is None else np.array(x0)
    x_new = np.zeros(n)
    residuals = []

    for iter in range(max_iterations):
        
        for i in range(n):
            x_new[i] = (b[i] - np.dot(A[i, :i], x_new[:i]) - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
        
        residuals.append(np.linalg.norm(A @ x_new - b))
        
        error = np.linalg.norm(x_new - x)
        if error < epsilon:
            return x_new
        
        x = np.copy(x_new)

    return x_new

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