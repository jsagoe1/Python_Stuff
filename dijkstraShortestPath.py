
# =============================================================================
# Graph represented by adjacency dictionary
# =============================================================================
graph = {

'a':{'b':3,'c':4, 'd':7},
'b':{'c':1,'f':5},
'c':{'f':6,'d':2},
'd':{'e':3, 'g':6},
'e':{'g':3, 'h':4},
'f':{'e':1, 'h':8},
'g':{'h':2},
'h':{'g':2}
}


def dijkstra(graph, start, goal):
    infinity = 99999999999
    shortestDistanceFromStart = {}  # to hold shortest distance to each vertex
    prevVertex = {}                 # to keep track of vertices leading to curVertex
    
    #set all vertices to infinity initially to start with
    for vertex in graph:
        shortestDistanceFromStart[vertex] = infinity
    #except start vertex, set to 0
    shortestDistanceFromStart[start] = 0
    
    unvisitedVertices = []            #to hold unvisited vertices as we go through graph
    visited = []                      #to hold visited vertices as we go through grapgh
    
    prevVertex[start] = None          # start has no prev node
    unvisitedVertices.append(start)
    
    #repeat until unvisited is empty
    while unvisitedVertices != []:
        #pop last element in Unvisited
        curVertex = unvisitedVertices.pop()
        #get connected vertices of curVertex
        for buddy, weight in graph[curVertex].items():
            #calculate distance from cur_vertex to buddy
            distance  = shortestDistanceFromStart[curVertex] + graph[curVertex][buddy]
            #update shortestdistance val if distance is less than stored
            if distance < shortestDistanceFromStart[buddy]:
                prevVertex[buddy] = curVertex
                shortestDistanceFromStart[buddy] = distance
            #add buddies to unvisited 
            if buddy not in unvisitedVertices and curVertex not in visited:
                unvisitedVertices.insert(0, buddy)
        #add curVertex to visited
        visited.append(curVertex)
        
    path = []               # to trace path
    cur = goal              # start from goal and trace back
    while cur!=None:
        path.insert(0,cur)
        cur = prevVertex[cur]
    if path[0] == start:
        return "-->".join(path)
    return []
    
            
                
            
    
print(dijkstra(graph, 'b', 'h'))
