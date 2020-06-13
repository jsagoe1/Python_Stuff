def dijkstra(graph, start, goal):
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
        
    unvisitedVertices = []          #to hold unvisited vertices as we go through graph
    visited = []                    #to hold visited vertices as we go through grapgh
    
    #set all vertices to infinity initially to start with
    for vertex in graph:
        shortestDistanceFromStart[vertex] = infinity
    #except start vertex, set to 0
    shortestDistanceFromStart[start] = 0
    
    prevVertex[start] = None          # start has no prev node, so set to None
    unvisitedVertices.insert(0,start)
    
    #repeat until unvisited is empty
    while unvisitedVertices != []:
        #pop last element in Unvisited, removes last element from unvisited
        curVertex = unvisitedVertices.pop()
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
                unvisitedVertices.insert(0, neighbour)
        #add curVertex to visited
        visited.append(curVertex)
        
    path = []                       # to trace path
    cur = goal                      # start from goal and trace back
    while cur!=None:
        if cur not in prevVertex:   #no path from start to goal
            print("No path from start to goal")
            return ([], 0)
        path.insert(0,cur)
        cur = prevVertex[cur]
    return (path, shortestDistanceFromStart[goal])
