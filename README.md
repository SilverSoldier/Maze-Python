# Maze-Python
Program in python which procedurally generates mazes using different algorithms, renders it with field-of-view and fog of war using libtcod and allows the user to move around to solve it.

## Maze generation
The procedural maze generation is done using the following algorithms.

### Randomized Kruskal's algorithm

Randomized Kruskal's is based on Kruskal's minimum spanning tree algorithm.

Explanation: http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm

Kruskal (```kruskal.py```) is implemented using disjoint set (union-find data structure) which I have written in ```disjoint_set.py```. The find operation uses path compression.

### Randomized Prim's Algorithm

Randomized Prim's is based on Prim's minimum spanning tree algorithm.

Explanation: http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm

Prim's method has been implemented in ```prim.py```.

### Binary Tree method

This method generates a very, very trivial maze with a south east bias (bias changes with implementation).

Explanation: http://weblog.jamisbuck.org/2011/2/1/maze-generation-binary-tree-algorithm

Binary tree method has been implemented in ```binarytree.py```.

The different methods of maze generation along with pros and cons are given by http://weblog.jamisbuck.org/under-the-hood/ very cleanly.

One can also checkout https://en.wikipedia.org/wiki/Maze_generation_algorithm which is the first search result and http://www.astrolog.org/labyrnth/algrithm.htm which talks about maze generation with much detail.

## Rendering maze and playing the game

Rendering maze can be done using libtcod.

To install libtcod follow 

http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_1#Setting_it_up

The famous Rogue like tutorial 

http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

gives a clear and detailed tutrial on how to create a rogue like from scratch.

I followed

**Part 1: Graphics** to install libtocd, set up game screen, print @ character and move it around.

**Part 2: The object and the map** to display a general map.

**Part 4: Field-of-view and exploration** to display the player's field-of-view and fog of war.

## Other features

The game gives the user the choice of maze generation algorithm to use when creating the maze.

**Displaying path upon completion**: Upon reaching the end point, the game displays the path the user took by adding a new member variable visited for each tile in the map, indicating whether the player visited the tile or not.

**Displaying correct solution upon exit**: When the player exits or gives up the game in the middle, the correct solution is found by performing a depth first search from the start to the finish.

Other features include **toggling fog of war** (using check_explore variable) and **displaying move count** in a **display panel** which also renders game messages.

(following http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_7).

## To Run Game

Ensure libtcod is installed to run the game, if not follow the instructions in the link above to install it.

To run, simply enter ```$python main.py``` in terminal to get the game screen.
