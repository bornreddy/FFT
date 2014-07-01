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
    data=data.astype('uint8')
    img=img.astype('uint8')
    data=np.asarray(img)

    im=Image.fromarray(data)
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
  return a*matrix+b
  #for row in matrix:
  #  for column in row:
  #    matrix[row][column]*=n_factor
  #return matrix  
