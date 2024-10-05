# Image compression using SVD decomposition
# Maryam Rezaee (ms.maryamrezaee@gmail.com)

from random import normalvariate
from math import sqrt

import numpy as np
from numpy.linalg import norm

from PIL import Image
import urllib.request
import io
import pathlib


def generateUnitVector(n):

    not_normalized = [normalvariate(0, 1) for i in range(n)]
    norm_var = sqrt(sum(x * x for x in not_normalized))
    normalized = [x / norm_var for x in not_normalized]

    return normalized


def generateSingularVector(matrix, epsilon=1e-10):

    n, m = matrix.shape
    e_i = generateUnitVector(min(n, m))
    last_v = None
    current_v = e_i

    if n > m:
        new_matrix = np.dot(matrix.T, matrix)
    else:
        new_matrix = np.dot(matrix, matrix.T)

    iterations = 0
    while True:

        iterations += 1
        last_v = current_v
        current_v = np.dot(new_matrix, last_v)
        current_v = current_v / norm(current_v)

        if abs(np.dot(current_v, last_v)) > 1 - epsilon:
            return current_v


def svdDecomposition(matrix, k=None, epsilon=1e-10):

    matrix = np.array(matrix, dtype=float)
    n, m = matrix.shape
    decomposition = []
    if k is None:
        k = min(n, m)

    for i in range(k):
        matrix_copy = matrix.copy()

        for u_i, singular_value, v_i in decomposition[:i]:
            matrix_copy -= singular_value * np.outer(u_i, v_i)

        if n > m:
            v_i = generateSingularVector(matrix_copy, epsilon=epsilon)
            u_not_normalized = np.dot(matrix, v_i)
            sigma = norm(u_not_normalized) 
            u_i = u_not_normalized / sigma
        else:
            u_i = generateSingularVector(matrix_copy, epsilon=epsilon)
            v_not_normalized = np.dot(matrix.T, u_i)
            sigma = norm(v_not_normalized)
            v_i = v_not_normalized / sigma

        decomposition.append((u_i, sigma, v_i))

    U, singular_values, V = [np.array(x) for x in zip(*decomposition)]
    return U.T, singular_values, V


def compressImage(image_path, k):
    
    img = Image.open(image_path)
    img_gray = img.convert('L')
    img_matrix = np.array(img_gray)

    # code for premade SVD from Python libraries:
    # U, sigma, V = np.linalg.svd(img_matrix)

    # computation by custom SVD written by me:
    U, sigma, V = svdDecomposition(img_matrix, k)
    sigma_truncated = np.diag(sigma[:k])
    U_truncated = U[:, :k]
    V_truncated = V[:k, :]

    comp_img_matrix = np.dot(U_truncated, np.dot(sigma_truncated, V_truncated))
    comp_img = Image.fromarray(comp_img_matrix.astype('uint8'), 'L')

    return comp_img


def getImage(address):

    if address.startswith(r"http://") or address.startswith(r"https://"):
        with urllib.request.urlopen(address) as url:
            image_data = url.read()

        image_bytes = io.BytesIO(image_data)
        name = "".join(address.split("/")[-1].split(".")[:-1])
        return image_bytes, name
            
    else:
        name = "".join(address.split("\\")[-1].split(".")[:-1])
        return address, name


if __name__ == "__main__":

    img_address = input("Enter the address of your image: ")
    k = int(input("Enter compression value k: "))

    img_path, img_name = getImage(img_address)
    comp_img = compressImage(img_path, k)
    path = pathlib.Path(__file__).parent.resolve()
    #print(path)
    path = str(path) + "\\" + str(img_name) + "_compressed.jpg"
    #print(path)
    comp_img.save(path)


# https://dfstudio-d420.kxcdn.com/wordpress/wp-content/uploads/2019/06/digital_camera_photo-1080x675.jpg
# I:\Misc\University\Matrix Computations\Project\SVD Image Compression - PY\image01.jpg