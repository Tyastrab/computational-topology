from itertools import combinations
import numpy as np
from appJar import gui


class Simplex(object):
     def __init__(self, name):
          self.name = list(name)        # typecase the name so it split into the vertices
          self.dim = len(name)-1        # the dimension is the number of vertices minus one
          self.neighbors = []
          self.wasVisited = False 
     
     def addNeighbor(self, s): 
          if s not in self.neighbors: 
               self.neighbors.append(s)

class SimplicialComplex(object):
     def __init__(self): 
          self.simplicies = dict()
          self.highest = 0
     
     def __str__(self): 
          ans = ""
          for i in self.simplicies:
               ans += i + ", "
          return ans
     
     def getS(self, name): 
          # if this is a new node, add it to the grapph
          if name not in self.simplicies: self.simplicies[name] = Simplex(name)
          
          #keep track of the highest dimension seen so far in the graph
          if self.simplicies[name].dim > self.highest: self.highest = self.simplicies[name].dim
          return self.simplicies[name] 
     
     
     def addEdge(self, name):
          self.getS("") # add empty string 
          x = [''.join(l) for i in range(len(name)) for l in combinations(name, i+1)] # all combinations of the simplex
          for i in x:
               self.getS(i)          
          for i in x:
               for j in x:
                    # if the simplicies are contained (in any combination) to another simplex
                    # and the simplicies are immeidately following dimensions 
                    # then make the two simplicies neighbors
                    if 0 not in [c in j for c in i] \
                       and self.simplicies[i].dim == self.simplicies[j].dim-1: 
                         self.simplicies[i].addNeighbor(self.simplicies[j])
                         self.simplicies[j].addNeighbor(self.simplicies[i]) 
                         
                    # if the simplicies has degree 0, make the empty simplex a neighbor
                    if self.simplicies[i].dim == 0: self.simplicies[i].addNeighbor(self.getS(""))
     
     def matrix(self):
          for p in range(self.highest,-1,-1):
               row = []
               col = []               
               for i in self.simplicies:
                    if self.simplicies[i].dim == p-1: 
                         row.append(i)
                    if self.simplicies[i].dim == p:  
                         col.append(i)
               print("Dimension ", p, "-", p-1, ":")
               print("Rows: ", row)
               print("Cols: ", col)
               self.matrixPopulation(row,col)
          print("Complete Boundary Matrix:")
          self.matrixPopulation(self.simplicies,self.simplicies)
               

     
     def matrixPopulation(self, row, col):
          matrix = [[0 for i in range(len(col))] for j in range(len(row))]
          r = -1
          for i in row:
               r += 1
               c = -1
               for j in col:
                    c +=1
                    if self.simplicies[i] in self.simplicies[j].neighbors:
                         matrix[r][c] = 1
               print(matrix[r])
          

def interactWithUser():

     simpComp = SimplicialComplex()
     print("To begin constructing your simplicial complex, enter the vertices of ")
     print("your first simplex. Continue entering new simplicies and type 'exit' ")
     print("when you're done: ")
     

     inp = input()
     while inp != "exit":
          simpComp.addEdge(inp)
          inp = input()
     simpComp.matrix()
          

def interactive():
     #this only works for one simplex at the moment
     app = gui("Simplicial Complex", "400x200")
     app.addLabel("title", "Welcome to Simplex")
     app.setLabelBg("title", "white")
     app.addLabelEntry("First Complex")
     
     
     
     def press(button):
          sc = SimplicialComplex()
          if button == "Finished":
               app.stop()
          else:
               usr = app.getEntry("First Complex")
               app.clearAllEntries()
               sc.addEdge(usr)
               sc.matrix()
     
     app.addButtons(["Submit", "Finished"], press)
     
     # start the GUI
     app.go()     

def __main():
     #sc = SimplicialComplex()
     #sc.addEdge('abcd')
     #sc.addEdge('de')
     #sc.addEdge('efg')
     #sc.matrix()
     
     
     print("Entering your own simplicial comlex")
     print("----------------------------------------")
     
     interactWithUser()  
     #interactive()


if __name__ == '__main__':
     __main()       
