from PIL_data import *
from FFT import *
COMPRESSION_PERCENT = 10
COMPRESSION_FACTOR = 1 #must be a power of two

def compress(filename = "images/small.jpg"):
  img = get_image(filename)
  #img is now a np.array of np.arrays with dimensions that are powers of two
  FFT_img = two_d_FFT(img)
  #new_width = (len(FFT_img[0])*(100-COMPRESSION_PERCENT))/100
  #new_height = (len(FFT_img)*(100-COMPRESSION_PERCENT))/100
  new_width=len(FFT_img[0])/COMPRESSION_FACTOR
  new_height=len(FFT_img)/COMPRESSION_FACTOR

  print new_width, new_height
  compressed_FFT_img = [[FFT_img[i][j] for i in range(new_height)] for j in range(new_width)]
  compressed_img=two_d_iFFT(compressed_FFT_img).real
  return_image(compressed_img)

compress()