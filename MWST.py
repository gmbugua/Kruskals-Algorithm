import sys
import math as mt

# DisjointSet()
# -------------
# initialization: U -> Universal Set indexed with the vertices of G
#                 All values except U[0] are set to -1 => V.p = v
#                 therefore the set is originally empty
# And a Youtube Video: https://www.youtube.com/watch?v=wU6udHRIkcc


class DisjointSet():

    def __init__(self, n):
        self.n = n
        self.U = [0]
        for i in range(n):
            self.U.append(-1)

    def Find_Set(self, x):
        if self.U[x] == -1:
            return x
        elif self.U[x] != -1:
            return self.Find_Set(self.U[x])

    def Union(self, u, v):
        parent_u = self.Find_Set(u)
        parent_v = self.Find_Set(v)
        self.U[parent_u] = parent_v

    # Cycle Detection
    # The idea is as follows:
    # For every Edge added to this Disjoint Set
    # We determine what subset the two vertices belong to
    # If at anytime they share the same set, then the edge
    # creates a cycle.
    def Cycle(self, e):
        u = self.Find_Set(e.getU())
        v = self.Find_Set(e.getV())
        if (u == v):
            return 1
        self.Union(u, v)

    def print_Set(self):
        for i in range(1, self.n + 1):
            print(self.U[i])

# MinPriortyQ()
# ------------
# init() Args:
# ------------
# g -> |E(G)|, a list of edge objects
# Different from other implementations
# => Keys are Edge Weights
# => Elements of Heap are Edges


class MinPriorityQ():

    # CONSTRUCTOR

    # pre: 1 <= n <= |E(G)|
    def __init__(self, g):
        self.Size = 0
        self.Heap = [0]
        for edge in g:
            self.HeapInsert(edge, edge.getW())

    # UTILITY
    def swap(self, i, j):
        tmp = self.Heap[i]
        self.Heap[i] = self.Heap[j]
        self.Heap[j] = tmp

    def i_Valid(self, i):
        return 0 if (i <= 0) or (i > len(self.Heap)) else 1

    # ACCESSOR

    def getSize(self):
        return self.Size

    # pre: 1 <= i <= |E(G)|
    def Parent(self, i):
        return self.Heap[mt.floor(i / 2)] if i_Valid(i) else -1

    # pre: 1 <= i <= |E(G)|
    def L_Child(self, i):
        return self.Heap[(2 * i)] if i_Valid(i) else -1

    # pre: 1 <= i <= |E(G)|
    def R_Child(self, i):
        return self.Heap[(2 * i) + 1] if i_Valid(i) else -1

    # pre: P is in Heap[1.....n]
    def P_Index(self, i):
        return int(mt.floor(i / 2))

    # pre: L is in Heap[1.....n]
    def L_Index(self, i):
        return (2 * i)

    # pre: R is in Heap[1.....n]
    def R_Index(self, i):
        return (2 * i) + 1

    # MANIPULATION

    def HeapMinimum(self):
        return self.Heap[1]

    # pre (n >= 1)
    def ExtractMin(self):
        minimum = self.HeapMinimum()
        self.swap(1, len(self.Heap) - 1)
        self.Heap.pop()
        self.Size = self.getSize() - 1
        self.Heapify(1)
        return minimum

    # pre (i >= 1)
    def Heapify(self, i):
        L = self.L_Index(i)
        R = self.R_Index(i)
        smallest = None

        if (L <= self.getSize()) and (self.Heap[L].getW() <= self.Heap[i].getW()):
            smallest = L
        else:
            smallest = i

        if (R <= self.getSize()) and (self.Heap[R].getW() <= self.Heap[smallest].getW()):
            smallest = R

        if (smallest != i):
            self.swap(i, smallest)
            self.Heapify(smallest)

    def HeapDecreaseKey(self, i, e, k):
        if (k < self.Heap[i].getW()):
            self.Heap[i] = e

        while (i >= 2) and (self.Heap[self.P_Index(i)].getW() > self.Heap[i].getW()):
            self.swap(i, self.P_Index(i))
            i = self.P_Index(i)

    def HeapInsert(self, e, k):
        self.Size += 1
        self.Heap.append(Edge(float("inf"), float(
            "inf"), float("inf"), float("inf")))
        self.HeapDecreaseKey(self.getSize(), e, k)

    def print_Heap(self):
        for i in range(1, self.getSize() + 1):
            self.Heap[i].print_Edge()

# Edge()
# ------------
# init() Args:
# ------------
# u -> start
# v ->  end
# w -> weight
# l -> label
# p -> parent
# r -> rank


class Edge():
    def __init__(self, u, v, w, l):
        self.u = u
        self.v = v
        self.weight = w
        self.label = l

    def getU(self):
        return self.u

    def getV(self):
        return self.v

    def getW(self):
        return self.weight

    def getL(self):
        return self.label

    def print_Edge(self):
        print("{}: ({}, {}) %.1f".format(
            self.label, self.u, self.v) % self.weight)

    def __str__(self):
        if self.label > 9:
            return "  {}: ({}, {}) %.1f\n".format(self.label, self.u, self.v) % self.weight
        else:
            return "   {}: ({}, {}) %.1f\n".format(self.label, self.u, self.v) % self.weight


Graph = list()
N = 0
M = 0

# FILE I/O
if len(sys.argv) != 3:
    print("Usage: {} <input file> <output file>".format(sys.argv[0]))
    sys.exit(2)  # exit(2) for command line errors


# Context Manager for Parsing File Input
# Reads in the file, line by line into a list
# Strips newline and leading spaces, then strips spaces inbetween edges
# Appends all edges to Graph List
with open(sys.argv[1], 'r') as f_in:

    f_in_contents = f_in.readlines()

    for i in range(len(f_in_contents)):
        f_in_contents[i] = (f_in_contents[i].strip('\n')).split(' ')

    # Cast all strings as integers
    for i in range(len(f_in_contents)):
        for j in range(len(f_in_contents[i])):
            f_in_contents[i][j] = int(f_in_contents[i][j])

    N = f_in_contents[0][0]
    M = f_in_contents[1][0]

    for i in range(2, len(f_in_contents)):
        e = Edge(f_in_contents[i][0], f_in_contents[i]
                 [1], f_in_contents[i][2], i - 1)
        Graph.append(e)

soln = list()

# Kruskal()
# args: Graph G, in my implmentation a list of all the edges
# Q => A priorty Queue of all the Edges in G
# F => A disjoint set initialized as the empty set


def Kruskal(G):
    Q = MinPriorityQ(G)
    F = DisjointSet(M)

    for i in range(M):
        e = Q.ExtractMin()

        if (F.Cycle(e) == 1):
            continue
        else:
            soln.append(e)


Graph_test = Graph.copy()
Kruskal(Graph_test)

Total_Weight = 0
for i in soln:
    Total_Weight += i.getW()

for i in range(len(soln)):
    soln[i] = str(soln[i])

soln.append("Total_Weight = %.1f" % Total_Weight)

with open(sys.argv[2], 'w') as f_out:
    f_out.writelines(soln)
