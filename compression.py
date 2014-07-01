from PIL_data import *
from FFT import *
COMPRESSION_PERCENT = 10

def compress(filename = "images/tiger.jpg"):
  img = get_image(filename)
  #img is now a np.array of np.arrays with dimensions that are powers of two
  FFT_img = FFT(img)
  new_width = (len(FFT_img[0])*(100-COMPRESSION_PERCENT))/100
  new_height = (len(FFT_img)*(100-COMPRESSION_PERCENT))/100
  compressed_FFT_img = [[FFT_img[i][j] for i in range(new_height)] for j in range(new_width)]
  print compressed_FFT_img

compress()