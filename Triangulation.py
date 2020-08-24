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

    # genus of the manifold - This only works if the surface is orientable
    def genus(self):
        return int((self.Euler()-2)/-2)

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
  
        # every node of the graph is a triangle
        class Triangle:
  
            def __init__(self, a, b, c):
                # The name of the Triangle - a concatenation of its vertices
                self.mu = ''.join([x for x in sorted([a,b,c])])
  
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
                self.neighbors = []
  
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
                def ORG(self):
                    return self.org
      
                # return the OrderedTriangle with a shared lead edge
                def FNEXT(self):
                    return self.fnext
      
                # calling the print function on an OrderedTriangle calls this
                def __str__(self):
                    return "(" + self.mu + ", " + str(self.i) + ")"

# This function interacts with the client, prompting the user
# to input triangles in order to store a triangulation
def interactWithUser():

    triangulation = Triangulation()
    print("We will begin by adding triangles to your triangulation. For each triangle")
    print("in your triangulation, enter the three vertices of the triangle separated ")
    print("by commas. Then press enter and repeat. When you are done adding triangles,")
    print("type 'exit'. Then you can begin running other tests on the triangulation.")
    
    inp = input("Type in the three vertices of your triangle separated by commas: ")
    while inp != "exit":
        node = inp.split(',')
        a = node[0].strip()
        b = node[1].strip()
        c = node[2].strip()
        triangulation.addTriangle(a,b,c)
        inp = input("Type in the three vertices of your triangle separated by commas: ")
    print("All the triangles have been added to the triangulation.")

# Triangulation of a torus - refer to Figure 2 in our report for more details
def torusTriangulation():
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

# Triangulation of a sphere, i.e. a tetrahedron
def sphereTriangulation():
    s = Triangulation()
    s.addTriangle('a', 'b', 'c')
    s.addTriangle('a', 'c', 'd')
    s.addTriangle('a', 'd', 'b')
    s.addTriangle('d', 'b', 'c')
    return s


def main():

    print("----------------------------------------")
    print("Properties of a Triangulation of a Torus")
    print("----------------------------------------")
    torus = torusTriangulation()
    print("A torus has", torus.numFaces(), "faces,", torus.numVertices(), \
          "vertices, and", torus.numEdges(), "edges")
    print("The Euler characteristic of a torus is: ", torus.Euler())
    print("The genus of a torus is: ", torus.genus())
    print("DFS: The graph of the triangulation of a torus has", \
          torus.graph.VISIT('abe'), "nodes")
    print()
  
    print("----------------------------------------")
    print("Properties of a Triangulation of a Sphere")
    print("----------------------------------------")
    sphere = sphereTriangulation()
    print("A sphere has", sphere.numFaces(), "faces,", sphere.numVertices(), \
          "vertices, and", sphere.numEdges(), "edges")
    print("The Euler characteristic of a sphere is: ", sphere.Euler())
    print("The genus of a sphere is: ", sphere.genus())
    print("DFS: The graph of the triangulation of a torus has", \
          sphere.graph.VISIT('abc'), "nodes")
    print()
    
    print("----------------------------------------")
    print("Follow the instructions to interact with the code")
    print("----------------------------------------")
  
    interactWithUser()

main()
