# SI-507-Final-Project
Course project for SI 507. This project aims to do flight search after the user gives their origin and destination.

# Data Source
```cache.py``` is used to generate all the required cached .json files. Three .json files in the repository are the results of this script.

```Graph.py``` is used to construct the graph structure and implement basic function of searching the shortest path between 2 airports.

```map.py``` contains functions used to draw figures based on the user's choice. 

# Requirements and packages
You need to install these packages first: ```webbrowser```, ```requests```, ```pandas```, ```BeautifulSoup```, ```Numpy```, ```matplotlib```, ```networkx``` and ```cartopy```.

You can find the installation of ```networkx``` here: https://networkx.org/documentation/stable/install.html

You can find the installation of ```cartopy``` here: https://scitools.org.uk/cartopy/docs/latest/installing.html


# How to run the project
To run my code, the users should run ```Graph.py``` file in Github repository. You can do it in command line: ```python Graph.py``` 

After doing this, the program will prompt some instructions of the project. The basic function of the code is to find the shortest flight path with minimum transfers between 2 cities. Firstly, it will ask the user to enter the IATA codes of the origin and destination. The program will then show the shortest flight path with minimum transfers. Then it will prompt and show 5 options for the users. For example, enter 1 if the user wants to see the network plot of the airports. Then it will show the corresponding presentations. You can see other displays after closing the previous presentation.

# Data Structure
I build a graph which connects the airports in the United States. The vertices are the airport. The edges are the airline connects 2 airports. It is a weighted and directed graph. The weight is the distance in miles between 2 airports. There are some extra attributes of the vertex in the graph such as the city and the state the vertex airport belongs to and the full name of the airport. 

Two json files contain the necessary data to construct the graph: ```airport_dict.json``` and ```airlines_us.json```. I defined 2 classes: ```Vertex``` and ```Graph``` in ```Graph.py```. And I use the function ```construct_graph``` in ```Graph.py``` to construct my graph of airports.

