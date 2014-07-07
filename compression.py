from PIL_data import *
from FFT import *
from cmath import *
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

def compress(filename="lena.mn",compression_factor=1):
  data = read_mn(filename)
  transformed_data = two_d_FFT(data)
  # print transformed_data[0][0:4]
  width,height = data.shape
  new_width = int(round(compression_factor*width))
  new_height = int(round(compression_factor*height))
  compressed_data = [[transformed_data[i][j] for j in range(new_width)] for i in range(new_height)]
  
  #splitting up complex numbers and normalizing both resulting matrices
  compressed_real,a_real,b_real = normalize(np.real(compressed_data))
  compressed_imag, a_imag, b_imag = normalize(np.imag(compressed_data))
  # compressed_normalized = np.around(compressed_real + 1j*(compressed_imag))
  write_mnc(filename+"c",compressed_real,compressed_imag, (width,height),(a_real,b_real,a_imag,b_imag))

def decompress(filename="lena.mnc"):
  data, original_size = read_mnc(filename)
  width, height = data.shape
  extended_width = original_size[0] - width
  extended_height = original_size[1] - height
  row_pad = np.zeros(extended_width)
  data = [np.hstack((row,row_pad)) for row in data]
  col_pad = np.zeros((extended_height,original_size[0]))
  data = np.vstack((data,col_pad))
  print data.shape
  iFFT_data = two_d_iFFT(data).real
  print iFFT_data[0]
  return iFFT_data



# iFFT_data = decompress()

# write_mn(iFFT_data)




# compress()