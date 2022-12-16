import json
import map
import requests
import webbrowser

class Vertex:
  """
  This is a class for vertex in the graph.
  """
  def __init__(self, key, city=None, state=None, airport=None):
    """
    The constructor of Vertex class.
    Parameters:
        key: the key of the vertex, IATA code of the airport
        city: name of the city where the airport in 
        state: name of the state where the airport in
        airport: the full name of the key airport
    """
    self.id = key
    self.connectedTo = {}
    self.city=city
    self.state=state
    self.airport=airport
  def addNeighbor(self, nbr, weight=0):
    """
    Add a neighbour bgr to the current key vertex with weight.
    """
    self.connectedTo[nbr] = weight
  def getId(self):
    return self.id
  def getWeight(self, nbr):
    return self.connectedTo[nbr]
  def getConnections(self):
    return self.connectedTo.keys()


class Graph:
    """
    This is the class for a graph data structure.
    """
    def __init__(self):
        """
        The constructor of Graph class.
        """
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key, city=None, state=None, airport=None):
        """
        Add a vertex of Vertex class to the graph.
        """
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,city,state,airport)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self, f, t, weight=0):
        """
        Connect 2 vertices f and t in the graph with an edge.
        Parameters:
            f: the starting vertex
            t: the end vertex
            weight: the weight of the edge
        """
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

def construct_graph():
    graph = Graph()
    f = open('airport_dict.json')
    airport_dict = json.load(f)
    for key in airport_dict.keys():
        graph.addVertex(key,airport_dict[key][1],airport_dict[key][0],airport_dict[key][2])
    f = open('airlines_us.json')
    data = json.load(f)
    for ori in data.keys():
        for des in data[ori][-1].keys():
            edge_weight=data[ori][-1][des]
            if edge_weight==[]: continue
            graph.addEdge(ori,des,edge_weight[0])
    return graph

def read_data():
    """
    Read the file: airlines_us.json
    Return: data containing the json file
    """
    f = open('airlines_us.json')
    data = json.load(f)
    return data

def shortest_path():
    """
    Print one shortest from origin to the destination
    Parameters:
        origin: departure airport's IATA code
        destination: arrival airport's IATA code
    """
    
    graph = construct_graph()
    
    origin=input("Input the IATA code of the origin: ")
    while not graph.__contains__(origin):
        print("Origin you entered is not valid. Please enter again.")    
        origin=input("Input the origin: ")
        
    destination=input("Input the IATA code of the destination: ")
    while not graph.__contains__(destination):
        print("Destination you entered is not valid. Please enter again.")  
        destination=input("Input the destination: ")
    tmp_dict={}
    queue=[origin]
    path = -1
    visited = set(origin)
    tmp_dict[origin] = ""
    while queue:
        tmp = []
        path += 1
        for location in queue:
            if location == destination:
                track=[location]
                while location!=origin:
                    track.append(tmp_dict[location])
                    location=tmp_dict[location]
                return (path,track[::-1], origin, destination)
            else:
                for node in graph.getVertex(location).getConnections():
                    node=node.getId()
                    if node in visited:
                        continue
                    visited.add(node)
                    tmp_dict[node] = location
                    tmp.append(node)
        queue = tmp

"""
Main function of the project. Deal with the inputs and the display options.
"""
print("Welcome to my flight search project! \nYou can enter the IATA codes of the departure and arrival aiports of your interests. For example, DTW and SFO. \nThen you will be shown the shortest path between these 2 airports and more advanced display options!\n ")

path, track, origin, destination = shortest_path()
print("\nThe shortest path between "+origin+" and "+destination+" is "+str(path))
for i in range(len(track)-1):
    print(track[i]+" ------> "+track[i+1])

print("\nEnter 1 if you want to see the network plot of the airports.")
print("Enter 2 if you want to see the flight routes on map. ")
print("Enter 3 if you want to see the route from origin to destination.")
print("Enter 4 for detailed flight information from origin to destination on website.")
print("Enter 5 to exit.\n")
option = input("Enter the option: ")

while int(option) != 5:
    if int(option) == 1:
        map.draw_network()
    elif int(option) == 2:
        map.draw_map()
    elif int(option) == 3:
        map.draw_line(track)
    elif int(option) == 4:
        url = "https://www.kayak.com/flights/"+origin+"-"+destination+"/2023-01-04?sort=bestflight_a&fs=airlines=-O2"
        print("\nLaunching: " + url + " in web browser...")
        webbrowser.open_new_tab(url)
    else: break
    option = input("Enter the option: ")

    
