# Graph-search
looks at various forms of graphs, much of the source material is taken from MIT course Artificial Intelligence 6.034

This program has various files associated with it:
  lab2.py- is where the entirety of my work on the assignment is. It features:
    Breath First Search
    Depth First Search
    Hill Climbing- uses heuristics to give priority to certain nodes
    Beam Search- limits scope of nodes explored at any one time
    Branch and Bound- uses path length to cut out paths that are too long
    A* uses heuristics and path lenghth to do all of the above minus beam search and BFS tactics
  search.py-
    Works with the nodes and their properties.
    An object to use the nodes
  tests.py-
    contains numerous test to try and evaluate the search algorithms in lab2
  tester.py-
    takes the tests and runs them
  graphs.py-
    Container for many test graphs to be used by lab2
