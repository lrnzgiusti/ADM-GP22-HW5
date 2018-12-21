# ADM-GP22-HW5 

## Visit the Wikipedia hyperlinks graph!

__Lorenzo Giusti, Federica Spoto, Vikranth Ale__

![bella](https://pbs.twimg.com/media/CNCowF1WEAAV1aZ.jpg)


In this homework we've performed an analysis of the reduced Wikipedia Hyperlink graph. In particular, given extra information about the categories to which an article belongs to, we are curious to rank the articles according to some criteria.


## Files
* [handler.py](https://github.com/lrnzgiusti/ADM-GP22-HW5/blob/master/handler.py): Is the *engine* of this homework. It contains a single big class that has all the useful methods to perform this analysis, in particular we've implemented three  different algorithms for the shortest path:
- bfs_monodirectional: The classical one-side bfs, you pick a source and a target and you visit the graph from the source to the target.
- shortest_path_bidir: The two-side bfs, a little explaination is inside the function. Actually is faster and it's deterministic so we've used this for the entire analysis.
- depth_wrapper_spanning_tree: This is a fancy random algorithm for build the bfs, you cannot find the explaination on the internet because this is a brand algorithm developed by us. You compute a generator for the spanning tree and the pick at random a path, if in the random path the source and the target are the ones that you're looking for, the path is correct. Otherwise pick another random path, you can prove that with the [Smoothed analysis](https://arxiv.org/pdf/cs/0111050.pdf) that the overall complexity is lower than the monodirectional bfs, but higher than the bidirectional bfs.

* [ADM-HW5-GP22.ipynb](https://github.com/lrnzgiusti/ADM-GP22-HW5/blob/master/ADM-HW5-GP22.ipynb)


