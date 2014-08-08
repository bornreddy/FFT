Compression Scheme
===

This repo contains an implementation of an FFT-based compression scheme. This product takes in an image, and outputs a compressed representation with a user-defined amount of "lossiness." We take advantage of the symmetries of the resulting matrix of the Fourier transform of a two-dimensional data set, allowing us to throw away entire portions of the frequency domain of an image. We then recover these frequencies the process of decompression before taking the inverse Fourier Transform of the data to recover an approximation of the original image. 


How to Use it
====

