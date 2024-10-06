# Maryam Rezaee - 981813088
# Finding Maximum Flow with Weighted Vertices

'''
This code contains two parts:
- Tools -->  classes / functions needed in body of code
- Body  -->  main body of code (defining graph, using tools, etc.)

WARNING: code contains a bug in Graph.maxflow() and does not work for
         converted graphs (ones where vertices are turned into edges)
         because the flow from the original vertex to itself gets
         ommited and path gets blocked.
'''

# -------------------------------- TOOLS --------------------------------


# class of graph objects
# uses adj matrix representation
# graph contains the traversal functions
class Graph:

    # construct necessary attributes
    def __init__(self, matrix):
        self.matrix = matrix         # remaining possible flow for edges
        self.vertices = len(matrix)  # number of vertices in graph


    # define function for iterative BFS of graph
    # needed to implement Elmonds-Karp algorithm
    def bfs(self, source, sink, parent):

        # initially all vertices are not visited
        # create the mark, then mark current one as visited
        visited = [False for i in range(self.vertices)]
        queue = [source] # to store the current path of BFS
        visited[source] = True

        # while queue not empty
        while queue:

            # keep removing first vertex in queue
            # and check its neighbours to see if
            # they are unvisited and can be visited
             v = queue.pop(0)
             for vertex, weight in enumerate(self.matrix[v]):
                 
                 if visited[vertex] == False and weight > 0:
                     queue.append(vertex)
                     visited[vertex] = True
                     # store last path taken to vertex
                     # meaning its parent in the entered array
                     parent[vertex] = v

                     # if the reached vertex is the sink
                     # stop BFS and return True meaning a
                     # path was found from source to sink
                     if vertex == sink:
                         return True

        # if bfs ends and no path is
        # found from source to sink
        return False


    # use Edmonds-Karp algorithm to solve
    # max flow problem using Ford-Fulkerson method
    def maxflow(self, source, sink):

        # initialise base variables
        # to store path to each vertex in this traversal:
        parent = [None] * self.vertices
        # to store each of the paths
        # taken from source to sink:
        paths = []
        # to find max flow:
        flow = 0

        # run BFS for all paths from source to sink and
        # keep updating remaining available flow in graph
        # until no more paths are possible and BFS is False
        while self.bfs(source, sink, parent):

            # initialise path flow as infinite
            # and use that to find min flow that
            # can remain unused in the found path
            pathflow = float('inf')

            # go backward from sink to source for this
            # and store the found path in an array
            end = sink
            thispath = [end]
            while end != source:
                pathflow = min(pathflow, self.matrix[parent[end]][end])
                end = parent[end]
                thispath.append(end)
            
            # update amounts for general flow
            # and the remaining possible flow
            # do the latter using the same backward method
            flow += pathflow
            end = sink
            while end != source:
                pre = parent[end]
                self.matrix[pre][end] -= pathflow
                self.matrix[end][pre] += pathflow
                end = parent[end]

            # reverse this path and store it
            thispath.reverse()
            paths.append(thispath)

        return flow, paths
        

# function to convert original graph to new
# so that weighted vertices become edges
# needed to be able to use Ford-Fulkerson method
def convert(graphdict):

    # since vertices are divided into two
    # the number of vertices doubles
    n = len(graphdict) * 2
    matrix = [[0 for i in range(n)] for j in range(n)]

    for vertex in graphdict:
        # divide vertex and put weight as weight of
        # the edge connecting the two new vertices
        v = ((vertex[0] + 1) * 2) - 1
        matrix[v - 1][v] = vertex[1]
        
        adjs = graphdict.get(vertex)
        for adj in adjs:
            # connect end of new edge to neighbours
            u = ((adj + 1) * 2) - 1
            matrix[v][u - 1] = adjs.get(adj)

    # return adjacency matrix of new graph
    # with elements as weight of edge
    return matrix


# -------------------------------- BODY ---------------------------------


if __name__ == '__main__':

    # an specific representation of graph where:
    # {(vertex, vertex weight) : {adj vertex : edge weight}}
    gdict = {(0,20) : {1:15, 2:17},
             (1,15) : {2:14, 3:20},
             (2,17) : {1:19, 3:30},
             (3,25) : {0:21, 1:18, 2:15}}
    # start and finish
    source, sink = 0, 3

    # convert so vertices are weighted edges
    # get the adjacency matrix of new graph
    gmatrix = convert(gdict)
    # update source and sink to fit new graph
    source = ((source + 1) * 2) - 2
    sink = ((source + 1) * 2) - 1

    # find max flow and its paths
    graph = Graph(gmatrix)
    flow, paths = graph.maxflow(source, sink)

    # update paths to fit original graph
    # do this using the fact that new
    # graph always has twice the vertices
    # so vertices can be mapped together
    ogpaths = []
    for path in paths:
        ogpath = []
        i = 0
        while i != len(path):
            ogpath.append(int(((i + 2) / 2) - 1))
            i += 2
        ogpaths.append(ogpath)

    print(f'The max flow equals {flow} and the data paths are {ogpaths}')
    
