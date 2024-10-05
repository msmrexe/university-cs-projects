# Performance comparison of 5 methods for solving systems of linear equations (Ax=b)
# Maryam Rezaee (ms.maryamrezaee@gmail.com)

import numpy as np
import time
import matplotlib.pyplot as plt

import GaussianElimination as GE
import GaussJordanElimination as GJE
import Jacobi as J
import GaussSeidel as GS
import SOR


# --------------------- TOOLS ---------------------


def hasSol(A, b):

    if np.linalg.det(A) == 0:
        return False
    
    n = A.shape[0]
    aug_matrix = np.column_stack((A, b))

    # if infinite solutions
    if (np.linalg.matrix_rank(A) == np.linalg.matrix_rank(aug_matrix) and
          np.linalg.matrix_rank(aug_matrix) < n):
        return False
    
    # if no solutions
    elif np.linalg.matrix_rank(aug_matrix) < np.linalg.matrix_rank(A):
        return False
    
    return True


def generateDiagDominant(n):

    A = np.random.rand(n, n)
    A = A + np.diag(np.sum(np.abs(A), axis=1))
    return A
    

# --------------------- RUN METHODS ---------------------

def runGE(x):

    y = []

    for n in x:
        A = np.random.rand(n, n)
        b = np.random.rand(n)

        while (hasSol(A, b) == False or 
               GE.canApply(A) == False):
            A = np.random.rand(n, n)
        
        start = time.perf_counter()
        sol_GE = GE.solve(A, b)
        end = time.perf_counter()
        
        y.append(end - start)
        
    return y


def runGJE(x):

    y = []

    for n in x:
        A = np.random.rand(n, n)
        b = np.random.rand(n)

        while (hasSol(A, b) == False or 
               GJE.canApply(A) == False):
            A = np.random.rand(n, n)
        
        start = time.perf_counter()
        sol_GJE = GJE.solve(A, b)
        end = time.perf_counter()
        
        y.append(end - start)
        
    return y


def runJ(x):

    y = []

    for n in x:
        A = generateDiagDominant(n)
        b = np.random.rand(n)

        while (J.canApply(A) == False):
            A = generateDiagDominant(n)
        
        start = time.perf_counter()
        sol_J = J.solve(A, b)
        end = time.perf_counter()
        
        y.append(end - start)
        
    return y


def runGS(x):

    y = []

    for n in x:
        A = generateDiagDominant(n)
        b = np.random.rand(n)

        while (GS.canApply(A) == False):
            A = generateDiagDominant(n)
        
        start = time.perf_counter()
        sol_GS = GS.solve(A, b)
        end = time.perf_counter()
        
        y.append(end - start)
        
    return y


def runSOR(x):

    y = []

    for n in x:
        A = generateDiagDominant(n)
        b = np.random.rand(n)

        while (SOR.canApply(A, 1) == False):
            A = generateDiagDominant(n)
        
        start = time.perf_counter()
        sol_GS = SOR.solve(A, b)
        end = time.perf_counter()
        
        y.append(end - start)
        
    return y


# --------------------- PLOT ---------------------


def runAndPlotTimes(limit):

    x = np.arange(2, limit+1)
    y_n, y_n2, y_n3 = x, x**2, x**3

    y_GE = runGE(x)
    y_GJE = runGJE(x)
    y_J = runJ(x)
    y_GS = runGS(x)
    y_SOR = runSOR(x)

    plt.figure().canvas.manager.set_window_title("Ax=b Solution Methods - Time Complexity")

    plt.subplot(121)

    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (s)")
    plt.plot(x, np.log10(y_GE), label="Gaussian Eliminaiton")
    plt.plot(x, np.log10(y_GJE), label="Gauss Jordan Eliminaiton")
    plt.plot(x, np.log10(y_J), label="Jacobi")
    plt.plot(x, np.log10(y_GS), label="Gauss Seidel")
    plt.plot(x, np.log10(y_SOR), label="SOR")

    ax = plt.gca()
    #ax.set_ylim([-0.2, 5])
    plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.subplot(122)

    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (s)")
    plt.plot(x, y_n, label="O(n)")
    plt.plot(x, y_n2, label="O(n^2)")
    plt.plot(x, y_n3, label="O(n^3)")

    ax = plt.gca()
    #ax.set_ylim([-0.2, 5])
    plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    runAndPlotTimes(15)