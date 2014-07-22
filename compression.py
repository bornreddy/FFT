from imageIO import *
from FFT import *
from cmath import *
import os

def compress(filename="lena.mn",output_filename="lena",compression_factor=.5):
  '''Writes a compressed mnc file. 
  The number of values kept is the (orginal number)*(compression_factor). 
  This version of the compression function acts on square images only.'''
  data = read_mn(filename)
  transformed_data = FFT(data)
  col_length=len(transformed_data) #also equals the number of rows
  row_length=len(transformed_data[0]) #also equals the number of columns
  #flatten the array:
  transformed_data=transformed_data.reshape((1,np.multiply(*transformed_data.shape)))[0]
  #given a compression factor, compression threshold is the value below which the...
  #function throws away frequency in the FFT data
  compression_threshold={'real':0,'imag':0}
  compression_threshold['real']=find_threshold(transformed_data.real,compression_factor)
  compression_threshold['imag']=find_threshold(transformed_data.imag,compression_factor)
  #by symmetry, the lower half of the data can be reproduced by the top half, excluding the first row
  upper_half=np.array(transformed_data[:(col_length/2+1)*row_length])
  #split FFT data into two pieces, real and imag
  uh_real=upper_half.real
  uh_imag=upper_half.imag 
  #throw away small values using compression threshold
  uh_real=np.array([i if abs(i)>compression_threshold['real'] else 0 for i in uh_real])
  uh_imag=np.array([i if abs(i)>compression_threshold['imag'] else 0 for i in uh_imag])
  #writes to mnc file
  write_mnc(output_filename+".mnc",np.around(uh_real).astype('int'),np.around(uh_imag).astype('int'), (len(data),len(data)),(1,0,1,0))

def find_threshold(data,compression_factor):
  '''Given a one-dimensional array and a compression_factor, finds 
  the threshold to throw away small values'''
  data_local=abs(data)
  data_local.sort()
  threshold_spot=int(float(len(data))*(1-compression_factor))
  if compression_factor==0:
    return data_local[len(data)-1]
  return data_local[threshold_spot]

def decompress(filename="lena.mnc"):
  '''reads a file, and rebuilds the ppm image and mn 
  representation based on the FFT data provided in the .mnc'''
  data, original_size = read_mnc(filename)
  width, height = data.shape
  iFFT_data = iFFT(data).real
  write_mn(iFFT_data,filename[:-4])
  write_ppm(iFFT_data,filename[:-4])

def generate_images():
  '''generates image in a range of compression factors for demo and testing'''
  #factors=np.linspace(0,1,41)
  factors=[.4];
  factor_data='';
  filesize_data=''
  outfile=open("output_files/data_file.txt","w+")
  for f in factors:
    print "processing factor: ",f
    #so .04 becomes "04"
    factor_string="{}{}".format(int(f*10),int(f*100)-10*int(f*10))
    output_filename="output_files/lena"+factor_string
    compress(filename="lena.mn",output_filename=output_filename,compression_factor=f)
    filesize=str(os.path.getsize("output_files/lena"+factor_string+".mnc"))+' '
    decompress(output_filename+".mnc")
    outfile.write(str(f)+'\t')
    outfile.write(filesize)
    outfile.write('\n')
  outfile.close()

generate_images()