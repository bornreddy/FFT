import numpy as np
import datetime
import sys

def FFT(A):
    '''Fast-Fourier-Transform up to two-dimensions. 
     Calls appropriate FFT for dimension of input'''
    #check to make sure input has the size of a power of two
    dims = A.shape
    for d in dims:
        if d<=1:
            print "FFT warning: data has unnecessary extra dimensions. Do some bracket counting!"
        if((d & d-1)!=0):
            print "Error in FFT: dimensions need to be powers of two. Try using zero-padding"
            return 
    if len(A.shape) == 1:
        print 1
        return FFT1(A)
    elif len(A.shape) == 2:
        print 2
        return FFT2(A)
    else:
        print "ERROR: FFT"
        print "This function only works on 1- and 2-dimensional input" 

def iFFT(A):
    '''Inverse Fast-Fourier-Transform up to two-dimensions. 
     Calls appropriate iFFT for dimension of input'''
    dims = A.shape
    for d in dims:
        if d<=1:
            print "FFT warning: data has unnecessary extra dimensions. Do some bracket counting!"
        if((d & d-1)!=0):
            print "Error in FFT: dimensions need to be powers of two. Try using zero-padding"
            return 
    if len(A.shape) == 1:
      return iFFT1(A)
    elif len(A.shape) == 2:
      return iFFT2(A)
    else:
      print "ERROR: iFFT"
      print "This function only works on 1- and 2-dimensional input" 

def FFT1(A):
  '''Classic Fast-Fourier-Transform acting on a 1-dimensional array
     Pseudocode adapted from CLRS FFT description'''
  n = len(A)
  if n == 1:
    return A
  w_n = np.exp(2*np.pi*1j/n) #nth root of unity
  w = 1
  a_even = A[0::2]
  a_odd = A[1::2]
  y_0 = FFT1(a_even) 
  y_1 = FFT1(a_odd)
  y=np.zeros(n)+0*1j
  for k in range(n/2):
    y[k] = y_0[k] + (w * y_1[k])
    y[k+(n/2)] = y_0[k] - (w * y_1[k])
    w *= w_n
  return y

def iFFT1(A):
  '''Classic inverse Fast-Fourier-Transform acting on a 1-dimensional array'''
  return np.conjugate(FFT1(np.conjugate(A)))/len(A)

def DFT1(A_col):
  '''Classic Discrete Fourier Transform implementation
  Simple matrix multiplication to change basis
  Acting on a one-dimensional array'''
  n = len(A_col)
  w_n = np.exp(2*np.pi*1j/n)
  V = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      V[i][j] = w_n**(i*j)
  return np.dot(V,A_col)

def iDFT1(A_col):
  '''Inverse Discrete Fourier Transform. 
     Acting on a one-dimensional array'''
  n = len(A_col)
  w_n = np.exp(2*np.pi*1j/n)
  # Vinv = np.array([[0.+1j]*n]*n)
  Vinv = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      Vinv[i][j] = w_n**(-i*j)/n
  return np.dot(Vinv,A_col)

def DFT(A):
  '''Discrete Fourier Transform of a matrix'''
  n = len(A)
  w_n = np.exp(2*np.pi*1j/n)
  V = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      V[i][j] = w_n**(i*j)
  return np.dot(np.dot(V,A),V)

def iDFT(A):
  '''Inverse Discrete Fourier Transform of a matrix'''
  n = len(A)
  w_n = np.exp(2*np.pi*1j/n)
  # Vinv = np.array([[0.+1j]*n]*n)
  Vinv = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      Vinv[i][j] = w_n**(-i*j)/n
  return np.dot(np.dot(Vinv,A),Vinv)

def FFT2(A):
  '''Two-dimensional Fast-Fourier-Transform 
     Takes an numpy array of numpy arrays'''
  num_rows = len(A)
  num_cols = len(A[0])
  output = np.array([[0.+1j]*num_cols for _ in range(num_rows)])
  for i in range(num_rows):
    output[i] = FFT1(A[i])
  output = output.T
  output2 = np.array([[0.+1j]*num_rows for _ in range(num_cols)])
  for i in range(num_cols):
    output2[i] = FFT1(output[i])
  return output2.T
  
def iFFT2(A):
  '''Two-dimensional inverse Fast-Fourier-Transform
      Takes a numpy array of numpy arrays'''
  num_rows = len(A)
  num_cols = len(A[0])
  output = np.array([[0.+1j]*num_cols for _ in range(num_rows)])
  for i in range(num_rows):
    output[i] = iFFT1(A[i])
  output = output.T
  output2 = np.array([[0.+1j]*num_rows for _ in range(num_cols)])
  for i in range(num_cols):
    output2[i] = iFFT1(output[i])
  return output2.T


print FFT(np.array([1,2]))