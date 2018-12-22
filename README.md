### Group 22
# ADM_HOMEWORK 5

### Visit the Wikipedia hyperlinks graph!

In this homework we have performed analysis of the **Wikipedia Hyperlink graph**. In particular, we have used the reduced version of the Wikipedia Graph provided by the SNAP group.

![bella](https://pbs.twimg.com/media/CNCowF1WEAAV1aZ.jpg)


### Getting Started

Download [WikiCat Hyperlink Graph](https://snap.stanford.edu/data/wiki-topcats.html) and extract information from the data provided in the files in the [webpage](https://snap.stanford.edu/data/wiki-topcats.html), also filter the categories which have more than 3500 articles and obtain their block ranking represented by the categories based on the shortesh path between the chosen input category and its closest neighbors.

We have calculated the shortest path between two nodes using search algorithms like One sided **Breadth First Search**, **Bi-Directional Breadth First Search** and **Depth Wrapper Spanning Tree**

We have used **Threading** concept to reduce the overall computational challenge that we encountered while doing this homework.

### Prerequisites

Importing libraries like Networkx to implement this graphs, Threading and Multiprocessing to reduce the overall computational workload on CPU ,Numpy to calculate mathematics,Json for files and collections to implement default dictionaries.


### Main Scripts

* [handler.py](https://github.com/lrnzgiusti/ADM-GP22-HW5/blob/master/handler.py): This is the main *engine* for this homework. It contains a single class that has all the useful methods to perform this analysis.

* [ADM-HW5-GP22.ipynb](https://github.com/lrnzgiusti/ADM-GP22-HW5/blob/master/ADM-HW5-GP22.ipynb): This is the Notebook file where all the Research questions have been answered.

#### Algorithms Explained !

* bfs_monodirectional: The classical one-side bfs, where you pick a source and a target node, and you traverse along the graph from the source to the target.
* shortest_path_bidir: The two-side bfs is more faster and is deterministic, we've used this for the entire analysis.
* depth_wrapper_spanning_tree: This is a fancy random algorithm to build the bfs algorithm, we have developed this brand new algorithm specially for this homework. First you compute a generator for the spanning tree and then pick at random a random unique path, if source and target are in this random path,then the path found by this algorithm is correct. Otherwise pick another random path, you can prove that with this [Smooth analysis](https://arxiv.org/pdf/cs/0111050.pdf) that the overall complexity is lower than the monodirectional bfs, but higher than the bidirectional bfs.


## Authors

*  **Lorenzo Giusti** 
*  **Federica Spoto**
*  **Vikranth Ale**

