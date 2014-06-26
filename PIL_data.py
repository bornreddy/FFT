from PIL import Image
import numpy as np


def get_image(filename):
  "opens image, converts to grayscale, and returns a np.array of np.arrays with intensity data"	
  img = Image.open(filename)
  img = img.convert('L')
  width,height = img.size
  data = img.getdata()
  output = np.array([])
  output = np.array([np.array([data[i] for i in range(n*width,(n+1)*width-1)]) for n in range(height)])
  print output
  return output



  
