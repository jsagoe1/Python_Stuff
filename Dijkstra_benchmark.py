## compare two different implemetations of Dijstra's shortest path
## algorithm on graph represented by adjacency list

from time import perf_counter_ns as pc
 
from random import choice, randint
import networkx
 
INF = float("inf")
 
 
def generate_path(start, goal, prev):
    path = []
    p = goal
    while p != start:
        path.append(p)
        if p not in prev:
            return []
        p = prev[p]
    path.append(start)
    path.reverse()
    return path
 
 
def dijkstra_wikipedia(graph, start, goal):
    Q = set(graph)
    dist = {v: INF for v in graph}
    dist[start] = 0
    prev = {}
 
    while Q:
        u = min(Q, key=dist.__getitem__)
        Q.remove(u)
 
        for v in graph[u]:
            alt = dist[u] + graph[u][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
 
    path = generate_path(start, goal, prev)
    return (path, dist[goal])
 
 
def dijkstra_self(graph, start, goal):
    def getPath(start, goal, prevVertex):
        path = []                       # to trace path
        cur = goal                      # start from goal and trace back
        while cur!=None:
            if cur not in prevVertex:   #no path from start to goal
                print("No path from start to goal")
                return ([], 0)
            path.insert(0,cur)
            cur = prevVertex[cur]
        return path   
        
    
    # check if start is same as goal
    if start in graph and start == goal:
        return ([start], 0)
    # check if start not present in graph
    if start not in graph:
        print("Error:'start' not present in graph")
        return ([],0)
        
    infinity = float("inf")         #Infinity
    shortestDistanceFromStart = {}  # to hold shortest distance to each vertex
    prevVertex = {}                 # to keep track of vertices leading to curVertex
        
    unvisitedVertices = {}          #to hold unvisited vertices as we go through graph
    visited = []                    #to hold visited vertices as we go through grapgh
    
    #set all vertices to infinity initially to start with
    for vertex in graph:
        shortestDistanceFromStart[vertex] = infinity
    #except start vertex, set to 0
    shortestDistanceFromStart[start] = 0
    
    prevVertex[start] = None          # start has no prev node, so set to None
    unvisitedVertices[start] = 0      # add start to unvisited
    
    #repeat until unvisited is empty
    while unvisitedVertices != {}:
        #pop last element in Unvisited, removes last element from unvisited
        curVertex = min(unvisitedVertices, key=unvisitedVertices.get)
        del unvisitedVertices[curVertex]
        #get connected vertices of curVertex
        for neighbour, weight in graph[curVertex].items():
            #calculate distance from cur_vertex to neighbour
            distance  = shortestDistanceFromStart[curVertex] + weight
            #update shortestdistance val if distance is less than stored distance
            if distance < shortestDistanceFromStart[neighbour]:
                shortestDistanceFromStart[neighbour] = distance
                #also update leading vertex to curVertex with shortest distance
                prevVertex[neighbour] = curVertex
            #add neighbours to unvisited 
            if neighbour not in unvisitedVertices and curVertex not in visited:
                unvisitedVertices[neighbour] = shortestDistanceFromStart[neighbour]
        #add curVertex to visited
        visited.append(curVertex)
    path = getPath(start,goal,prevVertex)
    return (path, shortestDistanceFromStart[goal])
 
 
def generate_problem(n_nodes=30, avg_degree=3):
    g = networkx.generators.dense_gnm_random_graph(n_nodes, avg_degree * n_nodes)
    for (u, v, w) in g.edges(data=True):
        w["weight"] = randint(1, 20)
 
    graph = {u: {v: w["weight"] for v, w in g[u].items()} for u in g}
 
    nodes = list(graph)
    start = choice(nodes)
    goal = choice(nodes)
    while start == goal:
        goal = choice(nodes)
 
    return g, graph, start, goal
 
 
def benchmark(label, f, graph, start, goal, n=100):
    st = pc()
    for _ in range(n):
        solution = f(graph, start, goal)
    et = pc()
 
    print(f"{label:20}: {(et-st)/(1e3 * n):.3f} µs")
    print("\tsolution: ", solution, "\n")
 
 
if __name__ == "__main__":
    for i in range(10):
        
        g, graph, start, goal = generate_problem(n_nodes=100, avg_degree=4)
        benchmark("Self    Impl", dijkstra_self, graph, start, goal)
        benchmark("Wikipedia Impl", dijkstra_wikipedia, graph, start, goal)
