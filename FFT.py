import numpy as np
import datetime


def FFT(A):
  n = len(A)
  if n == 1:
    return A
  w_n = np.exp(2*np.pi*1j/n)
  w = 1
  a_even = A[0::2]
  a_odd = A[1::2]
  y_0 = FFT(a_even) 
  y_1 = FFT(a_odd)
  y = [0]*n
  for k in range(n/2):
    y[k] = y_0[k] + (w * y_1[k])
    y[k+(n/2)] = y_0[k] - (w * y_1[k])
    w *= w_n
  return y
    
def main():
  a = datetime.datetime.now()
  A = [i for i in range(16)]
  print FFT(A)
  b = datetime.datetime.now()
  print "Time of FFT: ", b-a

main()
