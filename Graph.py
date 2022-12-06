import json

def read_data():
    f = open('airlines_us.json')
    data = json.load(f)
    return data

def shortest_path(origin, destination):
    data = read_data()
    tmp_dict={}
    queue=[origin]
    path = 0
    visited = set(origin)
    tmp_dict[origin] = ""
    while queue:
        tmp = []
        path += 1
        for location in queue:
            # if location in visited: continue
            if location == destination:
                track=[location]
                while location!=origin:
                    track.append(tmp_dict[location])
                    location=tmp_dict[location]
                return (path,track[::-1])
            else:
                # tmp+=list(zip(list(data[location[0]][-1].keys()),[location[0]]*len(list(data[location[0]][-1].keys()))))
                for node in list(data[location][-1].keys()):
                    if node in visited:
                        continue
                    visited.add(node)
                    tmp_dict[node] = location
                    tmp.append(node)
        queue = tmp

origin=input("Input the origin: ")
destination=input("Input the destination: ")
path, track = shortest_path(origin, destination)
print("The shortest path between "+origin+" and "+destination+" is "+str(path))
for i in range(len(track)-1):
    print(track[i]+" ------> "+track[i+1])
