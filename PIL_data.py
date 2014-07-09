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

def return_image(img,filename="output.jpg"):
    #arr=(img).astype('uint8')
    data=[]
    img=normalize(img)
    for row in img:
      data+=list(row)
    data=np.array(data)
    #data=data.astype('uint8')
    #img=img.astype('uint8')
    data=np.real(np.around(data))
    img=np.real(np.around(img))
    data=np.asarray(img)
    im=Image.fromarray(data)
    #im.show()
    print im.mode
    im = im.convert('L')
    #im.show()
    im.save(filename,"JPEG")

def normalize(matrix, maxcolor=255., mincolor=0,):
  #find the maximum
  m=[]#max 
  s=[]#min
  for row in matrix:
    m.append(max(row))
    s.append(min(row))
  matrix_max=max(m)
  matrix_min=min(s)
  #print matrix_max, matrix_min
  a=(mincolor-maxcolor)/(matrix_min-matrix_max)
  b=(matrix_min*maxcolor-matrix_max*mincolor)/(matrix_min-matrix_max)
  return a*matrix+b, a, b
  #for row in matrix:
  #  for column in row:
  #    matrix[row][column]*=n_factor
  #return matrix 

def denormalize(matrix,a,b):
  return (matrix-b)/a


#takes in ppm filename
def ppm2grey():
  ppmFile="lena.ppm"
  img = Image.open(ppmFile)
  img = img.convert('L')
  width,height = img.size
  data = list(img.getdata())
  # data_mat = [[data[i] for i in range(n*width,(n+1)*height)] for n in range(height)]
  data_mat = [data[n*width:(n+1)*width] for n in range(height)]
  
  f = open(ppmFile[:-4]+".mn",'w+')
  f.write(str(width)); f.write("\n"); f.write(str(height))
  f.write('\n')
  for row in data_mat:
    for column in row:
      f.write(str(column))
      f.write(" ")
    f.write(str("\n"))
    #f.write('\n')
  f.close()
  #this is a guess

def read_mn(filename="lena.mn"):
  f = open(filename)
  width = int(f.readline())
  height = int(f.readline())
  data = np.zeros((width, height))
  for i in range(height):
    data[i] = np.array(map(int,f.readline().split()))
  return np.array(data)

def write_mnc(filename,data_real, data_imag,original_size,norm_params):
  f = open(filename,"w+")
  f.write(str(original_size[0])); f.write('\n'); f.write(str(original_size[1]))
  f.write('\n')
  for i in norm_params:
    f.write(str(i) + "\n")
  for row in data_real:
    for column in row:
      f.write(str(int(np.around(column))))
      #f.write(str(column))
      f.write(" ")
    f.write(str("\n"))
  for row in data_imag:
    for column in row:
      f.write(str(int(np.around(column))))
      #f.write(str(column))
      f.write(" ")
    f.write(str("\n"))
    #f.write('\n')
  f.close()

def read_mnc(filename="lena.mnc"):
  f = open(filename,"r+");
  original_width = int(f.readline())
  original_height = int(f.readline())
  original_size = (original_width,original_height)
  a_real = float(f.readline())
  b_real = float(f.readline())
  a_imag = float(f.readline())
  b_imag = float(f.readline())
  data_array = [] #this will be filled in with the real matrix stacked over the imaginary matrix
  line = f.readline()
  while line:
    array_line = [float(i) for i in line.split()]
    data_array.append(array_line)
    line = f.readline()
  height = len(data_array)
  width=len(data_array[0])


  # denormalizing real and imag arrays
  real_array = np.array(data_array[:height/2])
  real_array = (real_array-b_real)/a_real
  imag_array = np.array(data_array[height/2:])
  imag_array = (imag_array-b_imag)/a_imag

  upper_half=real_array+1j*imag_array
  upper_rows,upper_columns=upper_half.shape

  FFT_data=np.vstack((upper_half,np.zeros((upper_rows-2,upper_columns))))
  
  #fill in the lower half
  new_row_num=upper_rows+1
  last_row_num=len(FFT_data)
  for row in range(new_row_num,last_row_num):
    for column in range(width):
      pair_row,pair_column=find_pair((row,column,width))
      new_val=np.conjugate(FFT_data[pair_row][pair_column])
      FFT_data[row][column]=new_val

  return FFT_data, original_size

def find_pair((j,k,N)):
  return ((N-j)%N,(N-k)%N)



def write_mn(data, filename="output_lena"):
  # clean up data to satisfy ppm requirements
  #data = [[int(data[i][j]) for j in range(len(data[0]))] for i in range(len(data))]
  data = [[float(data[i][j]) for j in range(len(data[0]))] for i in range(len(data))]
  width = len(data[0])
  height = len(data)
  # for i in range(width):
  #   for j in range(height):
  #     if data[j][i] > 255:
  #       data[j][i] = 255
  #     elif data[j][i] < 0:
  #       data[j][i] = 0
  # print data
  f = open(filename+".mn",'w+')
  f.write(str(len(data[0]))); f.write("\n"); f.write(str(len(data)))
  f.write('\n')
  for row in data:
    for column in row:
      f.write(str(column))
      f.write(" ")
    f.write(str("\n"))
    #f.write('\n')
  f.close()

def write_ppm(data, filename="output_lena"):
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
  print "i just wrote a ppm file called "+filename
#read_mnc()
# ppm2mn()
# data = read_mn()
# print data[0]
  #get size, 

