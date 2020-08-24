import matplotlib.pyplot as plt

# Helper function to print a matrix neatly
def printMatrix(m):
  for row in range(len(m)):
    print(m[row])

# Returns a list of the indices of the lowest ones of each column
# in the boundary matrix, None if it's a zero column
def getLows(matrix):

  # initialize all lowest ones to None
  lows = [None]*len(matrix[0])

  # go from bottom to top of each column
  for col in range(len(matrix[0])):
    for row in range(len(matrix)-1, -1, -1):

      # if we encounter a 1, this is the lowest one in the column, break
      if matrix[row][col] == 1:
        lows[col] = row
        break

  return lows

# Returns whether there is a column in a matrix to the left of column 
# j whose lowest one is at the same index as the lowest one of j
def equalLow(lows, j):
  # for each column j0 to the left of j
  for j0 in range(j):
    # if j0 is not a zero column and j0 has the same lowest one and j
    if lows[j0] and lows[j0] == lows[j]:
      return j0
  return None

# Compute reduced matrix R from a boundary matrix
def REDUCE(boundaryMatrix):

  R = boundaryMatrix
  lows = getLows(R)

  # for each column
  for j in range(len(R[0])):

    # if this column is not a zero column
    if lows[j]:

      # (fencepost loop)
      # get the index of the column that has the same low
      j0 = equalLow(lows, j)

      # while exists j0 < j s.t. low(j0) = low(j)
      while j0 != None:

        lows[j] = None

        # going from bottom to top of the column
        for row in range(len(R)-1, -1, -1):
        
          # add column j0 to column j with modular arithmetic
          R[row][j] = (R[row][j] + R[row][j0]) % 2

          # update lows[j]
          if not lows[j] and R[row][j] == 1:
            lows[j] = row

        # update the boolean
        j0 = equalLow(lows, j)

  return R


# Compute zp (rank of p-cycles) and bp (rank of p-boundaries) for each dimension
# then use them to compute Betti numbers
# Simplices is a list, at each index p in the list there is a tuple representing
# the column numbers of the first and last columns that correspond to simplices
# of dimension p
def computeBetti(R, simplices):

  lows = getLows(R)

  # initialize to zeroes
  zp = [0]*len(simplices)
  bp = [0]*len(simplices)
  betti = [0]*len(simplices)

  # for each dimension
  for a in range(len(simplices)):
    # for each of the simplices of that dimension
    for col in range(simplices[a][0], simplices[a][1]+1):
      # if the corresponding column is a zero column
      if not lows[col]:
        # add it to zp for that dimension
        zp[a] += 1

  # for each dimension
  for b in range(len(simplices)-1):
    # bp is the number of non-zero columns corresponding to (p+1)-simplices
    # (number of columns corresponding to (p+1)-simplices) - 
    # (number of zero columns corresponding to (p+1)-simplices)
    bp[b] = (simplices[b+1][1] - simplices[b+1][0] + 1) - zp[b+1]

  # the Betti number of each dimension p is zp - bp
  for c in range(len(betti)):
    betti[c] = zp[c] - bp[c]

    print(str(c) + "-Betti number: " + str(betti[c]))

  return zp, bp, betti

# Find the points in the p-dimensional persistence diagram
# Inputs are a dimension p, a reduced matrix R, and simplices
# (For explanation of simplices, see comment before computeBetti)
def persistence(p, R, simplices):

  # initialize
  lows = getLows(R)
  points = []

  # for each row i corresponding to a p-simplex
  for i in range(simplices[p][0], simplices[p][1]+1):

    # if row i contains a "lowest one"
    if i in lows:
      # get the column j that row i has the "lowest one" of
      j = lows.index(i)
      # if j corresponds to a (p+1) simplex
      if j >= simplices[p+1][0] and j <= simplices[p+1][1]+1:
        # add i,j to the list of points
        points += [(i+1,j+1)]

    # if column i is a zero column (has no lowest one)
    if not lows[i]:
      # if row i doesn't have a lowest one in it
      if i not in lows:
        # add (i, infinity) to the persistence diagram
        points += [(i+1, 'INF')]

  print("Points in the " + str(p) + "-dimensional persistence diagram: ", end = "")
  print(points)
  
  return points

# compute a norm for a persistence diagram as the sum of the areas of triangles
# created by drawing vertical and horizontal lines from each point to the diagonal
# (beta version - not sure how is best to handle INF values)
def norm(p, points):
  norm = 0

  for point in points:
    # use 20 to represent infinity (not a perfect solution)
    if point[1] == "INF":
      norm += .5*((20 - point[0])**2)
    else:
      norm += .5*(point[1] - point[0])**2

  print(str(p) + "-dimensional L1-norm: " + str(norm))
  return norm

# given a list of points, create a persistence diagram
def plot(points):
  x = []
  y = []

  # create a list of x values and a list of y values
  for p in points:
    x.append(p[0])
    # use 20 in place of infinity
    if p[1] == 'INF':
      y.append(20)
    else:
      y.append(p[1])

  # set up the axes
  plt.xlim(left = 0, right = 20)
  plt.ylim(bottom = 0, top = 20)
  plt.xlabel("Birth")
  plt.ylabel("Death")

  # add the diagonal to the plot
  plt.plot(range(0,21), range(0,21))
  # plot the points
  plt.scatter(x,y)

  plt.show()


def main():
  # EXAMPLE 1, UNFILLED TRIANGLE
  print("EXAMPLE 1: UNFILLED TRIANGLE\n")

  boundaryMatrix = [[0,0,0,1,1,0],
                    [0,0,0,1,0,1],
                    [0,0,0,0,1,1],
                    [0,0,0,0,0,0],
                    [0,0,0,0,0,0],
                    [0,0,0,0,0,0]]

  # 0-simplices are represented by rows/columns 0-2, 1-simplices by 3-5
  simplices = [(0,2), (3,5)]

  print("Boundary Matrix:")
  printMatrix(boundaryMatrix)

  R = REDUCE(boundaryMatrix)
  print("\nReduced Matrix R:")
  printMatrix(R)
  print()

  computeBetti(R, simplices)
  print()
  pers0 = persistence(0, R, simplices)
  pers1 = persistence(1, R, simplices)
  print()

  norm(0, pers0)
  norm(1, pers1)  

  plot(pers0)
  plot(pers1)


  # EXAMPLE 2, FILLED TRIANGLE
  print("\nEXAMPLE 2: FILLED TRIANGLE")

  bm2 = [[0,0,0,1,1,0,0],
         [0,0,0,1,0,1,0],
         [0,0,0,0,1,1,0],
         [0,0,0,0,0,0,1],
         [0,0,0,0,0,0,1],
         [0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0]]

  simplices = [(0,2), (3,5), (6,6)]

  print("\nBoundary Matrix:")
  printMatrix(bm2)

  R2 = REDUCE(bm2)
  print("\nReduced Matrix R:")
  printMatrix(R2)
  print()

  computeBetti(R2, simplices)
  print()

  pers0 = persistence(0, R2, simplices)
  pers1 = persistence(1, R2, simplices)
  pers2 = persistence(2, R2, simplices)
  print()

  norm(0, pers0)
  norm(1, pers1)
  norm(2, pers2)

  plot(pers0)
  plot(pers1)
  plot(pers2)


  # EXAMPLE 3, UNFILLED TETRAHEDRON
  print("\nEXAMPLE 3: UNFILLED TETRAHEDRON")

  bm3 = [[0,0,0,0,1,1,1,0,0,0,0,0,0,0],
         [0,0,0,0,1,0,0,1,1,0,0,0,0,0],
         [0,0,0,0,0,1,0,1,0,1,0,0,0,0],
         [0,0,0,0,0,0,1,0,1,1,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,1,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,1,0,1],
         [0,0,0,0,0,0,0,0,0,0,1,0,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,1,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,1,1],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

  simplices = [(0,3), (4,9), (10,13)]

  print("\nBoundary Matrix:")
  printMatrix(bm3)

  R3 = REDUCE(bm3)
  print("\nReduced Matrix R:")
  printMatrix(R3)
  print()

  computeBetti(R3, simplices)
  print()
  pts0 = persistence(0, R3, simplices)
  pts1 = persistence(1, R3, simplices)
  pts2 = persistence(2, R3, simplices)

  plot(pts0)
  plot(pts1)
  plot(pts2)

  # EXAMPLE 4, FILLED TETRAHEDRON
  print("\nEXAMPLE 4: FILLED TETRAHEDRON")

  bm4 = [[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
         [0,0,0,0,1,0,0,1,1,0,0,0,0,0,0],
         [0,0,0,0,0,1,0,1,0,1,0,0,0,0,0],
         [0,0,0,0,0,0,1,0,1,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
         [0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

  simplices = [(0,3), (4,9), (10,13), (14,14)]

  print("\nBoundary Matrix:")
  printMatrix(bm4)

  R4 = REDUCE(bm4)
  print("\nReduced Matrix R:")
  printMatrix(R4)
  print()

  computeBetti(R4, simplices)
  print()
  p0 = persistence(0, R4, simplices)
  p1 = persistence(1, R4, simplices)
  p2 = persistence(2, R4, simplices)

  plot(p0)
  plot(p1)
  plot(p2)

main()
