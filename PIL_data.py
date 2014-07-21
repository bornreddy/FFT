import numpy as np

def ppm2mn(ppmFile="lena.ppm"):
  '''Converts a file from ppm to mn.
     Records only greyscale, not rgb values.'''
  img = Image.open(ppmFile)
  img = img.convert('L')
  width,height = img.size
  data = list(img.getdata())
  data_mat = [data[n*width:(n+1)*width] for n in range(height)]
  f = open(ppmFile[:-4]+".mn",'w+')
  f.write(str(width)); f.write("\n"); f.write(str(height))
  f.write('\n')
  for row in data_mat:
    for column in row:
      f.write(str(column))
      f.write(" ")
    f.write(str("\n"))
  f.close()

def read_mn(filename="lena.mn"):
  '''returns data from an mn file as a two-dimensional numpy array'''
  f = open(filename)
  width = int(f.readline())
  height = int(f.readline())
  data = np.zeros((width, height))
  for i in range(height):
    data[i] = np.array(map(int,f.readline().split()))
  return np.array(data)

def write_mnc(filename,data_real, data_imag,original_size,norm_params):
  '''takes in a filename, a numpy array split into real and imaginary parts, and original size'''
  '''!!!!! get rid of norm params!!!!!''' 
  f = open(filename,"w+")
  f.write(str(original_size[0])); f.write('\n'); f.write(str(original_size[1]))
  f.write('\n')
  for i in norm_params:
    f.write(str(i) + "\n")
  #do run length encoding
  data_real=run_length_encode(data_real);
  data_imag=run_length_encode(data_imag);
  for i in data_real:
    f.write(str(i)+" ")
  for i in data_imag:
    f.write(str(i)+" ")
  f.close()

def run_length_encode(data):
  '''replaces subarray of zeros of length n with 'zn' '''
  edata=[]
  in_zero_run=False;
  count=0
  for ind,c in enumerate(data):
    #take care of last element separately
    if(ind==len(data)-1):
      if(c==0 and in_zero_run):
        count+=1
        edata.append('z'+str(count))
      if(c==0 and not in_zero_run):
        edata.append(0)
      elif(c!=0 and in_zero_run):
        edata.append('z'+str(count))
        edata.append(c)
      elif(c!=0 and not in_zero_run):
        edata.append(c)
      return edata

    elif (c==0 and in_zero_run):
      count+=1;
    elif(c==0 and not in_zero_run):
      in_zero_run=True
      count=1
    elif(c!=0 and in_zero_run):
      in_zero_run=False
      if(count==1):
        edata.append('0')
      else:
        edata.append('z'+str(count))
      edata.append(c)
      count=0
    elif(c!=0 and not in_zero_run):
      edata.append(c)
  


def run_length_unencode(data):
  '''inserts an array n zeros in place of string 'zn'''
  udata=[]
  for c in data:
    if c[0]=='z':
      zlen=int(c[1:])
      for i in range(zlen):
        udata.append(0.0)
    else: #its just a number
      udata.append(float(c))
  return np.array(udata)

#print run_length_unencode(run_length_encode([0,0,1,0,0,1,0]))

def read_mnc(filename="lena.mnc"):
  '''reads a .mnc file and returns a complex, two-dimensional array of 
  frequency data and the original image size'''
  f = open(filename,"r+");
  original_width = int(f.readline())
  original_height = int(f.readline())
  original_size = (original_width,original_height)
  a_real = float(f.readline())
  b_real = float(f.readline())
  a_imag = float(f.readline())
  b_imag = float(f.readline())
  data_array=f.readline().split() #a massive, long data array
  data_array=np.array([i for i in data_array])
  data_array=run_length_unencode(data_array)
  #split into real and imaginary parts
  da_real=data_array[0:len(data_array)/2].reshape((original_height/2+1,original_width))
  da_imag=data_array[len(data_array)/2:].reshape((original_height/2+1,original_width))
  upper_half=da_real+1j*da_imag
  upper_rows,upper_columns=upper_half.shape
  FFT_data=np.vstack((upper_half,np.zeros((upper_rows-2,upper_columns))))
  #fill in the lower half
  new_row_num=upper_rows+1
  last_row_num=len(FFT_data)
  for row in range(new_row_num,last_row_num):
    for column in range(original_width):
      pair_row,pair_column=find_pair((row,column,original_width))
      new_val=np.conjugate(FFT_data[pair_row][pair_column])
      FFT_data[row][column]=new_val
  return FFT_data, original_size

def find_pair((j,k,N)):
  ''' symmetries of two-dimensional FFT data array'''
  return ((N-j)%N,(N-k)%N)

def write_mn(data, filename="output_lena"):
  '''Takes in an array of float image data and writes to mn format.'''
  # clean up data to satisfy mn requirements
  data = [[int(data[i][j]) for j in range(len(data[0]))] for i in range(len(data))]
  width = len(data[0])
  height = len(data)
  f = open(filename+".mn",'w+')
  f.write(str(len(data[0]))); f.write("\n"); f.write(str(len(data)))
  f.write('\n')
  for row in data:
    for column in row:
      f.write(str(column))
      f.write(" ")
    f.write(str("\n"))
  f.close()

def write_ppm(data, filename="output_lena"):
  '''Takes in an array of float image data and writes to a ppm format.
     Float truncation may lead to a tiny bit of quality loss.'''
  # clean up data
  data = [[int(data[i][j]) for j in range(len(data[0]))] for i in range(len(data))]
  width = len(data[0])
  height = len(data)
  for i in range(width):
    for j in range(height):
      if data[j][i] > 255:
        data[j][i] = 255
      elif data[j][i] < 0:
        data[j][i] = 0
  #print data
  f = open(filename+".ppm",'w+')
  f.write("P3\n")
  f.write(str(width) + " " + str(height) + "\n")
  f.write("255\n")
  for row in data:
    for column in row:
      out_string = (str(column) + " ")*3
      f.write(out_string)
  f.close()
