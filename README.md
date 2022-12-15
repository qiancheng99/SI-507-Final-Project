# SI-507-Final-Project
Course project for SI 507. This project aims to do flight search after the user gives their origin and destination.

# Data Source
```cache.py``` is used to generate all the required cached .json files. Three .json files in the repository are the results of this script.

```Graph.py``` is used to construct the graph structure and implement basic function of searching the shortest path between 2 airports.

```map.py``` contains functions used to draw figures based on the user's choice. 

# Requirements and packages

# How to run the project
To run my code, the users should run ```Graph.py``` file in Github repository. You can do it in command line: ```python Graph.py``` 

After doing this, the program will prompt some instructions of the project. The basic function of the code is to find the shortest flight path with minimum transfers between 2 cities. Firstly, it will ask the user to enter the IATA codes of the origin and destination. The program will then show the shortest flight path with minimum transfers. Then it will prompt and show 5 options for the users. For example, enter 1 if the user wants to see the network plot of the airports. Then it will show the corresponding presentations. You can see other displays after closing the previous presentation.

