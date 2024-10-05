# Project Overview

This project was defined as the main final project for the Master's course of Matrix Computations (2023 | Semester 4021) at Sharif University of Technology. The code was implemented using Python programming language but with minimal usage of predefined Python functions and libraries.

## Topic

Implementation of Grayscale Image Compression Using SVD Decomposition

## Description

The SVD decomposition was implemented from scratch without using any pre-built libraries. Due to my interest in image processing and the significance of SVD decomposition, achieving efficiency was key. Therefore, the details of the implementation idea were derived from optimization methods discussed in a highly referenced textbook after research (the PDF file is available in the folder), which resulted in a relatively efficient algorithm. The final SVD decomposition was then applied to a grayscale image, leveraging the top singular values for image estimation and compression.

To enhance usability, the input was expanded to provide the option to input an image address from local drive or the internet, automatically identify address type and process the image, convert it to grayscale, compress it, and save the output with the original name appended by "_compressed" in the same folder as the code.  

### Note

- Although I was interested in extending the method to coloured images, I discontinued this work due to time limitations.
- The compression for large images takes a few minutes, so patience is needed.
- Whatever the size, the resulting quality is directly relevant to the chosen K and the main objects of the image will always be clear, even when the redundant areas are extremely low in quality.
