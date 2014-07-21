import numpy as np
import datetime
import sys

def FFT1(A):
  "Classic FFT acting on a 1-dimensional array"
  
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

def iFFT_recur(A):
  n = len(A)
  if n == 1:
    return A
  w_n = np.exp((-1)*2*np.pi*1j/n)
  w = 1
  a_even = A[0::2]
  a_odd = A[1::2]
  y_0 = FFT1(a_even)
  y_1 = FFT1(a_odd)
  #y = [0]*n
  y=np.zeros(n)+0*1j
  for k in range(n/2):
    y[k] = y_0[k] + (w * y_1[k])
    y[k+(n/2)] = y_0[k] - (w * y_1[k])
    w *= w_n
  return y

def iFFT(A):
  return np.conjugate(FFT1(np.conjugate(A)))/len(A)


def DFT1(A_col):
  n = len(A_col)
  w_n = np.exp(2*np.pi*1j/n)
  #V = np.array([[0.+1j]*n]*n)
  V = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      V[i][j] = w_n**(i*j)
  return np.dot(V,A_col)

def DFT(A):
  n = len(A)
  w_n = np.exp(2*np.pi*1j/n)
  #V = np.array([[0.+1j]*n]*n)
  V = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      V[i][j] = w_n**(i*j)
  return np.dot(np.dot(V,A),V)

def iDFT(A):
  n = len(A)
  w_n = np.exp(2*np.pi*1j/n)
  # Vinv = np.array([[0.+1j]*n]*n)
  Vinv = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      Vinv[i][j] = w_n**(-i*j)/n
  return np.dot(np.dot(Vinv,A),Vinv)

def iDFT1(A_col):
  n = len(A_col)
  w_n = np.exp(2*np.pi*1j/n)
  # Vinv = np.array([[0.+1j]*n]*n)
  Vinv = np.array([[0.+1j]*n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      Vinv[i][j] = w_n**(-i*j)/n
  return np.dot(Vinv,A_col)

#DFT=np.vectorize(DFT1)
#iDFT=np.vectorize(iDFT1)

def two_d_FFT(A):
  num_rows = len(A)
  num_cols = len(A[0])
  # output = np.array([[0]*num_col]*num_rows)
  output = np.array([[0.+1j]*num_cols for _ in range(num_rows)])
  for i in range(num_rows):
    output[i] = FFT1(A[i])
  output = output.T
  # output2 = np.array([[0]*num_rows]*num_col)
  output2 = np.array([[0.+1j]*num_rows for _ in range(num_cols)])
  for i in range(num_cols):
    output2[i] = FFT1(output[i])
  return output2.T
  
def two_d_iFFT(A):
  num_rows = len(A)
  num_cols = len(A[0])
  output = np.array([[0.+1j]*num_cols for _ in range(num_rows)])
  for i in range(num_rows):
    output[i] = iFFT(A[i])
  output = output.T
  output2 = np.array([[0.+1j]*num_rows for _ in range(num_cols)])
  for i in range(num_cols):
    output2[i] = iFFT(output[i])
  return output2.T
  
    
def test_iFFT(A):
    return np.conjugate(FFT1(np.conjugate(A)))/len(A)

def main():
  
  A=np.random.rand(8,8)
  print "input:" 
  print A

  B=two_d_FFT(A)
  print "FFT1(A):"
  print np.around(B)
main()
