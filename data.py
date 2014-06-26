

MAX_COLOR = 255

# class pixel(object):
#   def __init__(self,color):
#       if type(color) == type(1):
#         self.color = [color,color,color]
#       else:
#          self.color = color 

def normalize(matrix):
  m = []
  s = []
  for row in matrix:
    m.append(max(row))
    s.append(min(row))
  matrix_max = max(m)
  matrix_min = min(s)
  n_factor = MAX_COLOR/(matrix_max-matrix_min)
  for row in matrix:
    for column in row:
        matrix[row][column] *= n_factor
  return matrix




screen=[[1,2,3,0]]*4

def create_ppm():
  f=open("testing.ppm",'w')
  f.write("P3\n")
  f.write("4 4\n")
  f.write("3\n")
  for row in screen:
      for pixel in row:
          f.write(" ".join(str(pixel)*3)+" ")
      f.write("\n")
  f.close()