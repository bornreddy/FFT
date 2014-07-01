from PIL import Image
import numpy as np


def get_image(filename="images/tiger.jpg"):
  "opens image, converts to grayscale, and returns a np.array of np.arrays with intensity data"	
  width_extended = int()
  height_extended = int()
  img = Image.open(filename)
  img = img.convert('L')
  width,height = img.size
  n = 1
  while True:
    if width <= 2**n:
      width_extended = 2**n
      break
    else:
      n += 1
  n = 1
  while True:
    if height <= 2**n:
      height_extended = 2**n
      break
    else:
      n += 1
  row_pad = list(np.zeros(width_extended-width)) #zeros at the end of each row so we have length as a power of two
  extra_rows = [np.zeros(width_extended) for _ in range(height_extended-height)]
  data = img.getdata()
  output = np.array([])
  output = np.array([np.array([data[i] for i in range(n*width,(n+1)*width)]+row_pad) for n in range(height)]+extra_rows)
  print "got image, padded dimensions with zeros"
  return output



  
