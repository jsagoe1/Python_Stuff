def dijkstra_reddit(graph, start, goal):
    #to get the path from start to goal
    def getPath(start, goal, prevVertex):
        path = []                       
        cur = goal                      
        while cur!=None:
            if cur not in prevVertex:   
                print("No path from start to goal")
                return ([], 0)
            path.insert(0,cur)
            cur = prevVertex[cur]
        return path
        
           
    if start in graph and start == goal:
        return ([start], 0)
    if start not in graph:
        print("Error:'start' not present in graph")
        return ([],0)
        
    infinity = float("inf")         
    shortestDistanceFromStart = {}  
    prevVertex = {}                 
    unvisitedVertices = {}          
    visited = []
                        
    for vertex in graph:
        shortestDistanceFromStart[vertex] = infinity
    shortestDistanceFromStart[start] = 0
    
    prevVertex[start] = None          
    unvisitedVertices[start] = 0
          
    while unvisitedVertices != {}:
        curVertex = min(unvisitedVertices, key=unvisitedVertices.get)
        del unvisitedVertices[curVertex]
        for neighbour, weight in graph[curVertex].items():
            distance  = shortestDistanceFromStart[curVertex] + weight
            if distance < shortestDistanceFromStart[neighbour]:
                shortestDistanceFromStart[neighbour] = distance
                prevVertex[neighbour] = curVertex
            if neighbour not in unvisitedVertices and curVertex not in visited:
                unvisitedVertices[neighbour] = shortestDistanceFromStart[neighbour]
        visited.append(curVertex)
    path = getPath(start,goal,prevVertex)
    return (path, shortestDistanceFromStart[goal])
