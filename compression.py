from PIL_data import *
from FFT import *
from cmath import *
import matplotlib.pylab as plt
COMPRESSION_PERCENT = 10
COMPRESSION_FACTOR = 2 #must be a power of two

def jpg_compress(filename = "images/small.jpg"):
  filename = "images/tiger.jpg"
  img = get_image(filename)
  #img=np.array([[img[x][y] for y in range(8)] for x in range(8)])
  #print img
  #print "dims of im", len(img),len(img[0]), type(img)
  #img=np.zeros((10,10))
  #img[5]=img[5]+100
  #print img
  #img is now a np.array of np.arrays with dimensions that are powers of two
  FFT_img = two_d_FFT(img)
  #new_width = (len(FFT_img[0])*(100-COMPRESSION_PERCENT))/100
  #new_height = (len(FFT_img)*(100-COMPRESSION_PERCENT))/100
  new_width=len(FFT_img[0])/COMPRESSION_FACTOR
  new_height=len(FFT_img)/COMPRESSION_FACTOR
  #print new_width, new_height
  compressed_FFT_img = np.zeros((new_width, new_height))
  compressed_FFT_img = [[FFT_img[j][i] for i in range(new_height)] for j in range(new_width)]
  compressed_img=np.real(two_d_iFFT(compressed_FFT_img))
  #print "dims of im", len(img),len(img[0])
  #print "dims of new img", len(compressed_img),len(compressed_img[0]),type(compressed_img)
  # np.around(compressed_img) #doesn't mutate 
  return_image(compressed_img)

def compress(filename="lena.mn",compression_percent=1,compression_threshold=10000):
  data = read_mn(filename)
  transformed_data = two_d_FFT(data)
  #print "DC component is ", transformed_data[0][0]
  #by symmetry, the lower half of the data can be reproduced by the top half +1 row
  #upper_half=np.array([transformed_data[i] for i in range(len(transformed_data)/2+1)])

  upper_half=np.array([row for row in transformed_data[:len(transformed_data)/2+1]])
  #throw away small values
  for row_num,row in enumerate(upper_half):
    for col_num,col in enumerate(row):
      if abs(col.real)<compression_threshold:
        upper_half[row_num][col_num]=upper_half[row_num][col_num].imag*1j
      if abs(col.imag)<compression_threshold:
        upper_half[row_num][col_num]=upper_half[row_num][col_num].real

  upper_half_imag=upper_half.imag
  upper_half_real=upper_half.real
  

  
  write_mnc(filename+"c",upper_half_real,upper_half_imag, (len(data),len(data)),(1,0,1,0))

def decompress(filename="lena.mnc"):
  #read mnc - must be changed to construct the "data" matrix using bad_notation(x_n-j,_n-k) rule
  #no need to store original_size. 
  data, original_size = read_mnc(filename)
  width, height = data.shape
  #pad with zeros to full size
  # extended_width = original_size[0] - width
  # extended_height = original_size[1] - height
  # row_pad = np.zeros(extended_width)
  # data = [np.hstack((row,row_pad)) for row in data]
  # col_pad = np.zeros((extended_height,original_size[0]))
  # data = np.vstack((data,col_pad))
  # print data.shape
  iFFT_data = two_d_iFFT(data).real

  write_mn(iFFT_data)
  write_ppm(iFFT_data)
  #return iFFT_data



# iFFT_data = decompress()

# write_mn(iFFT_data)



compress()
decompress()