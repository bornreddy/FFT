from PIL_data import *
from FFT import *
from cmath import *
import matplotlib.pylab as plt
import os
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

def compress(filename="lena.mn",output_filename="lena",compression_factor=.5):
  data = read_mn(filename)
  transformed_data = two_d_FFT(data)
  col_length=len(transformed_data) #also equals the number of rows
  row_length=len(transformed_data[0]) #also equals the number of columns
  #flatten the array:
  transformed_data=transformed_data.reshape((1,np.multiply(*transformed_data.shape)))[0]

  compression_threshold={'real':0,'imag':0}
  compression_threshold['real']=find_threshold(transformed_data.real,compression_factor)
  compression_threshold['imag']=find_threshold(transformed_data.imag,compression_factor)

  #by symmetry, the lower half of the data can be reproduced by the top half +1 row
  #upper_half=np.array([transformed_data[i] for i in range(len(transformed_data)/2+1)])
  upper_half=np.array(transformed_data[:(col_length/2+1)*row_length])

  #split into two pieces, real and imag
  uh_real=upper_half.real
  uh_imag=upper_half.imag 
  #throw away small values
  uh_real=np.array([i if abs(i)>compression_threshold['real'] else 0 for i in uh_real])
  uh_imag=np.array([i if abs(i)>compression_threshold['imag'] else 0 for i in uh_imag])
  
  #shape them back into two dimensional things
  #uh_real=uh_real.reshape((col_length/2+1,row_length))
  #uh_imag=uh_imag.reshape((col_length/2+1,row_length))

  write_mnc(output_filename+".mnc",np.around(uh_real).astype('int'),np.around(uh_imag).astype('int'), (len(data),len(data)),(1,0,1,0))

def find_threshold(data,compression_factor):
  #data=abs(data.reshape((1,np.multiply(*data.shape)))[0]) #flatten the array for sorting
  #assume a 1d data shape
  data_local=abs(data)
  data_local.sort()
  threshold_spot=int(float(len(data))*(1-compression_factor))
  #print "threshold_spot:",threshold_spot
  #print "threshold_value:",data[threshold_spot]
  if compression_factor==0:
    return data_local[len(data)-1]
  return data_local[threshold_spot]

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

  write_mn(iFFT_data,filename[:-4])
  write_ppm(iFFT_data,filename[:-4])
  #return iFFT_data



# iFFT_data = decompress()

# write_mn(iFFT_data)
def generate_images():
  factors=np.linspace(0,1,20)
  factor_data='';
  filesize_data=''
  outfile=open("output_files/data_file.txt","w+")
  for f in factors:
    print "processing factor: ",f
    #so .04 becomes "04"
    factor_string="{}{}".format(int(f*10),int(f*100)-10*int(f*10))
    output_filename="output_files/lena"+factor_string
    compress(filename="lena.mn",output_filename=output_filename,compression_factor=f)
    #factor_data=(str(f)+' ')
    filesize=str(os.path.getsize("output_files/lena"+factor_string+".mnc"))+' '
    decompress(output_filename+".mnc")
    outfile.write(str(f)+'\t')
    outfile.write(filesize)
    outfile.write('\n')

  outfile.close()
  

generate_images()