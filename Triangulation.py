# Triangulation of a compact, connected 2-manifold without boundary
class Triangulation:

    # a triangulation contains a list of vertices and a graph of triangles
    def __init__(self):
        # vertices are represented by characters and stored in a set
        self.vertices = set()
        # triangles are stored in a graph structure
        self.graph = self.Graph()

    # client uses this method to input a triangulation,
    # passing in the three vertices of each triangle
    def addTriangle(self, a, b, c):
        self.vertices.add(a)
        self.vertices.add(b)
        self.vertices.add(c)
        self.graph.addNode(a, b, c)


    # number of vertices in the triangulation
    def numVertices(self):
        return len(self.vertices)

    # number of faces in the triangulation
    def numFaces(self):
        return len(self.graph.nodes)

    # number of edges in the triangulation
    def numEdges(self):
      # each triangle has 3 edges, each edge is shared by 2 triangles
        return int((3*len(self.graph.nodes))/2)
  
    # Euler characteristic of the manifold
    def Euler(self):
        return self.numVertices() - self.numEdges() + self.numFaces()
    
    # genus of the manifold
    def genus(self):
        orientable = self.graph.isOrientable() 
        if orientable: return self.manifold((self.numFaces() - 2*self.numVertices() +4)/4, orientable)
        else: return self.manifold((self.numFaces() - 2*self.numVertices() +4)/2, orientable)
    
    def manifold(self, genus, orientable):
        if genus == 0.0 and orientable: return "orientable sphere"
        if genus == 1.0 and orientable: return "orientable torus"
        if genus == 2.0 and orientable: return "orientable double-torus"
        if genus == 1.0 and not orientable: return "non-orientable projective plane"
        if genus == 2.0 and not orientable: return "non-orientable Klein Bottle"  
        if orientable: ans = "orientable "
        else: ans = "non-orientable "
        ans += str(genus) + "-hole manifold"
        return ans
    

    # a structure to store triangles of a triangulation
    class Graph:

        # The nodes of a graph are triangles, arcs are stored implicitly
        # The arcs of a graph represent shared edges between triangles
        def __init__(self):
            # A dictionary whose keys are Triangle names and values are Triangle objects
            self.nodes = {}

        # add a node to the graph
        def addNode(self, a, b, c):
            n = self.Triangle(a, b, c)
  
            # If this triangle shares an edge with another, add an arc between them. 
            # Every triangle has 3 neighbors since the manifold is without boundary.
            for node in self.nodes.values():
                if n.sharesEdgeWith(node):
                    n.addArc(node)
                    node.addArc(n)
  
            # insert this node in the dictionary of nodes
            self.nodes[n.mu] = n
            
        def looper(self):
            for node in self.nodes.values():
                print(node.mu)          
  
        # reset the isVisited attribute of every Triangle in the graph to False
        def resetFlags(self):
            for node in self.nodes.values():
                node.isVisited = False
  
        # visit all the nodes in the graph with a DFS, counting the number of nodes
        def VISIT(self, mu):
            answer = self.nodes[mu].visit()
            # reset flags so future calls to this method will be accurate
            self.resetFlags() 
            return answer
        
            
        def isOrientable(self):
            for triangle in self.nodes.keys():             # loops through triangulation
                x = self.fnext(triangle[0:2], triangle)    # considers the three edges      
                y = self.fnext(triangle[1:3], triangle)
                z = self.fnext(triangle[0:1] + triangle[2:3], triangle)
                ans = x and y and z
                if ans == False: return False
            return True

                
        def fnext(self, given, original):
            a = given[0] 
            b = given[1] 
            for node in self.nodes.keys():  
                if node != original:
                    x = node.find(a)              # if both vertices are found, we know this
                    y = node.find(b)              # triangle has a shared edge        
                    if x > -1 and y > -1:         # 
                        if x > y: return True     # if the order of the vertices are reversed
                        else: return False        # this triangle is orientable               

        
        # every node of the graph is a triangle
        class Triangle:
  
            def __init__(self, a, b, c):
                # The name of the Triangle - a concatenation of its vertices
                self.mu = ''.join([x for x in ([a,b,c])])
                #print("Mu's:", self.mu)
  
                # The symmetry group of the Triangle
                self.symGroups = [self.OrderedTriangle(self.mu,0), \
                                  self.OrderedTriangle(self.mu,1), \
                                  self.OrderedTriangle(self.mu,2), \
                                  self.OrderedTriangle(self.mu,4), \
                                  self.OrderedTriangle(self.mu,5), \
                                  self.OrderedTriangle(self.mu,6)]
               
      
                # the 3 vertices of this Triangle
                self.vertices = [a, b, c]
  
                # the 3 neighbors of this Triangle - 3 other Triangle objects
                self.neighbors = [self,self,self]
  
                # set the lead vertices of the OrderedTriangle objects in the
                # symmetry group of this Triangle
                self.orgs = [a, b, c, None, b, c, a]
                for OrdTri in self.symGroups:
                    OrdTri.org = self.orgs[OrdTri.i]
  
                # a boolean flag, used in traversing the Graph
                self.isVisited = False
  
            # determine whether 2 triangles share an edge (i.e. share 2 vertices)
            def sharesEdgeWith(self, other):
                sharedVertices = 0
                for vertex in self.vertices:
                    if vertex in other.vertices:
                        sharedVertices += 1
                return sharedVertices == 2
  
            # add an arc between two nodes of a graph
            def addArc(self, other):
                self.neighbors.append(other)
  
            # Textbook code for a DFS that visits every node of a graph,
            # recursively counting the number of nodes in the graph
            def VISIT(self, numNodes = 0):
                if not self.isVisited:
                    self.isVisited = True
                    numNodes += 1
                    for neighbor in self.neighbors:
                        numNodes += neighbor.VISIT()
                    return numNodes
                return 0
  
            # More concise version of DFS - called by VISIT in Graph
            def visit(self):
                if not self.isVisited:
                    self.isVisited = True
                    return 1 + self.neighbors[0].VISIT() + \
                    self.neighbors[1].VISIT() + self.neighbors[2].VISIT()
                return 0           
                    
  
            # a triangle with an ordering of its vertices
            class OrderedTriangle:

                
            
                def __init__(self, mu, i):
                    # the name of the Triangle that this OrderedTriangle is in
                    self.mu = mu
                    # i = iota, an element of {0, 1, 2, 4, 5, 6}
                    self.i = i    
                    # the Ordered Triangle that shares a lead edge with this one
                    # (not implemented in this code)
                    self.fnext = None
                    # the lead vertex of this OrderedTriangle, implemented in Triangle
                    self.org = None
  
                # advance the lead edge of an OrderedTriangle
                
                def ENEXT(self):
                    if i <= 2:
                        return OrderedTriangle(self.mu, (self.i+1) % 3)
                    return OrderedTriangle(self.mu, (self.i+1) % 3 + 4)
      
                # reverse the direction of a lead edge of a OrderedTriangle
                def SYM(self):
                    return OrderedTriangle(self.mu, (self.i+4) % 8)
      
                # return the lead vertex of this OrderedTriangle
                #def ORG(self):
                    #return self.org
                    
                def ORG(self):
                    return self.mu[0:1]
      
                # return the OrderedTriangle with a shared lead edge
                def FNEXT(self):
                    return self.fnext
      
                # calling the print function on an OrderedTriangle calls this
                def __str__(self):
                    return "(" + self.mu + ", " + str(self.i) + ")"
                
                def isOrientable(self, i):
                    if not self.isVisited:
                        self.isVisited = True  # remember that we visited this triangle
                        x = self.isOrientable(FNEXT(SYM(self, i)))
                        y = self.isOrientable(FNEXT(ENEXT(SYM(self, i))))
                        z = self.isOrientable(FNEXT(ENEXT(ENEXT(SYM(self, i)))))
                        return x and y and z   # if even one edge fails, this will return False
                

# This function interacts with the client, prompting the user
# to input triangles in order to store a triangulation
def interactWithUser():

    triangulation = Triangulation()
    print("To begin your triangulation, enter the vertices as an ordered triangle")
    print("Enter vertices seperated by commas and type exit when you're done: ")
    
    inp = input()
    while inp != "exit":
        node = inp.split(',')
        a = node[0].strip()
        b = node[1].strip()
        c = node[2].strip()
        x = a+b+c
        triangulation.addTriangle(a,b,c)
        inp = input()
    print(x)
    print("Triangulation manifold: ", triangulation.genus())

# Triangulation of a torus - refer to Figure 2 in our report for more details
def torusTriangulation():
    s = Triangulation()
    s.addTriangle('b','a','e')
    s.addTriangle('e','h','b')
    s.addTriangle('c','b','h')
    s.addTriangle('h','i','c')
    s.addTriangle('d','c','i')
    s.addTriangle('i','j','d')
    s.addTriangle('j','e','a')
    s.addTriangle('a','d','j') #end of 1
    s.addTriangle('h','e','f')
    s.addTriangle('f','k','h')
    s.addTriangle('i','h','k')
    s.addTriangle('k','l','i')
    s.addTriangle('j','i','l')
    s.addTriangle('l','z','j')
    s.addTriangle('e','j','z')
    s.addTriangle('z','f','e') #end of 2
    s.addTriangle('k','f','g')
    s.addTriangle('g','n','k')
    s.addTriangle('l','k','n')
    s.addTriangle('n','o','l')
    s.addTriangle('z','l','o')
    s.addTriangle('o','p','z')
    s.addTriangle('f','z','p')
    s.addTriangle('p','g','f') #end of 3
    s.addTriangle('n','g','a')
    s.addTriangle('a','b','n')
    s.addTriangle('o','n','b')
    s.addTriangle('b','c','o')
    s.addTriangle('p','o','c')
    s.addTriangle('c','d','p')
    s.addTriangle('g','p','d')
    s.addTriangle('d','a','g') # end of 4
    return s

def sphereTriangulation():
    s = Triangulation()
    s.addTriangle('c','a','f') 
    s.addTriangle('f','g','c')
    s.addTriangle('d','c','g')
    s.addTriangle('g','h','d')
    s.addTriangle('b','d','h')
    s.addTriangle('h','f','b')
    s.addTriangle('g','f','e')
    s.addTriangle('e','i','g')
    s.addTriangle('h','g','i')
    s.addTriangle('i','j','k')
    s.addTriangle('f','h','j')
    s.addTriangle('j','e','f')
    s.addTriangle('i','e','b')
    s.addTriangle('c','b','i')
    s.addTriangle('j','i','c')
    s.addTriangle('c','d','j')
    s.addTriangle('e','j','d')
    s.addTriangle('d','a','e')
    return s    
    

    
# Triangulation of a sphere, i.e. a tetrahedron
def kleinBottleTriangulation():
    t = Triangulation()
    t.addTriangle('a', 'b', 'e')
    t.addTriangle('b', 'e', 'h')
    t.addTriangle('b', 'c', 'h')
    t.addTriangle('h', 'c', 'i')
    t.addTriangle('c', 'd', 'i')
    t.addTriangle('d', 'i', 'j')
    t.addTriangle('d', 'a', 'j')
    t.addTriangle('a', 'j', 'e') #End of row 1
    t.addTriangle('e', 'f', 'h')
    t.addTriangle('f', 'h', 'k')
    t.addTriangle('h', 'i', 'k')
    t.addTriangle('i', 'k', 'l')
    t.addTriangle('l', 'i', 'j')
    t.addTriangle('l', 'j', 'm')
    t.addTriangle('m', 'j', 'e')
    t.addTriangle('e', 'f', 'm') #End of row two
    t.addTriangle('f', 'g', 'k')
    t.addTriangle('g', 'k', 'n')
    t.addTriangle('n', 'k', 'l')
    t.addTriangle('n', 'l', 'o')
    t.addTriangle('m', 'l', 'o')
    t.addTriangle('m', 'o', 'p')
    t.addTriangle('p', 'm', 'f')
    t.addTriangle('g', 'f', 'p') #End of row three
    t.addTriangle('a', 'g', 'n')
    t.addTriangle('a', 'b', 'n')
    t.addTriangle('n', 'b', 'o')
    t.addTriangle('b', 'c', 'o')
    t.addTriangle('c', 'o', 'p')
    t.addTriangle('c', 'd', 'p')
    t.addTriangle('p', 'g', 'd')
    t.addTriangle('d', 'a', 'g')    
    return t
    

def main():   

    torus = torusTriangulation()
    print("Torus triangulation Manifold:" ,torus.genus())
    
    sphere = sphereTriangulation()
    print("Sphere triangulation Manifold:" ,sphere.genus())    
  

    kb = kleinBottleTriangulation()
    print("Klein Bottle triangulation Manifold:", kb.genus())
    
    
    print()    
    print("----------------------------------------")
    print("Follow the instructions to interact with the code")
  
    interactWithUser()

main()
