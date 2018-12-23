from collections import deque, defaultdict
import numpy as np
import networkx as nx
import json
from threading import Thread
from multiprocessing import cpu_count

class Handler():
    """docstring for Handler"""

    def __init__(self):
        """
        Constructior of the class that handle all the utilities for the homework
        You read the input category from the standard input 
        Then you build the categories in a defaultdict taken if the articles inside that category are more than 3500
        In the end we read the graph from the wiki-topcats-reduced file that contains only the directed edges of the graph
        """
        self.input_category = input()
        self.categories = defaultdict(set)
        with open('wiki-topcats-categories.txt', 'r') as f:
            for row in f:
                splitted_row = row.split(' ')
                if len(splitted_row[1:]) > 3500:
                    self.categories[  splitted_row[0][9:-1]   ] = set(splitted_row[1:])
        self.inverted_index =  {node : cate for cate in self.categories for node in self.categories[cate]}
        self.G = nx.read_edgelist('wiki-topcats-reduced.txt', nodetype=str, 
                                  delimiter='\t', create_using=nx.DiGraph())


    def bfs_monodirectional(self, source, target):
        """
        BFS is an algorithm for traversing or searching in a graph.
        It starts at the source node s,
        and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.
        
        The bfs can simulate a dijkstra algorithm if and only if the weight of the edges are ALL equal to 1
        """
        if not(self.G.has_node(source) or self.G.has_node(target)):
            return []
        visited = dict()#is the list containing the nodes of the shortest path between the source and the target
        path = []
        visited[source] = 'null'
        to_visit = deque([source])
        while(to_visit):
            visiting = to_visit.pop()
            vicini = set(self.G.neighbors(visiting))
            visited.update({vicino : visiting for vicino in vicini if vicino not in visited})
            to_visit.extendleft(vicini)
            if target in vicini:
                chiave = target
                path.append(target)
                while visited[chiave] != 'null':
                    path.append(visited[chiave])
                    chiave = visited[chiave]
                return path[::-1]


    def shortest_path_bidir(self, source, target):
        
        """
        
        This is a wrapper for the two-sided bfs.
        It stores the results in a list of vertexes that are orderd in the way you've visited the graph.
        
        """
        
        if source not in self.G or target not in self.G:
            return None

        result = self.pred_succ(source, target)
        if result is None:
            return None
        elif result is np.inf:
            return np.inf
        pred, succ, w = result
        # build path from pred+w+succ
        path = []
        # from source to w
        while w is not None:
            path.append(w)
            w = pred[w]
        path.reverse()
        # from w to target
        w = succ[path[-1]]
        while w is not None:
            path.append(w)
            w = succ[w]

        return path


    def pred_succ(self, source, target):

        """
        
        Bidirectional search is a graph search algorithm which find smallest path form source to goal vertex. 
        It runs two simultaneous search:

        1. Forward search form source/initial vertex toward goal vertex
        2. Backward search form goal/target vertex toward source vertex
        Bidirectional search replaces single search graph(which is likely to grow exponentially) with two smaller sub graphs 
        one starting from initial vertex and other starting from goal vertex. The search terminates when two graphs intersect.
        
        """
        
        # does BFS from both source and target and meets in the middle
        if target == source:
            return ({target: None}, {source: None}, source)


        G_pred = self.G.pred
        G_succ = self.G.succ

        # predecesssor and successors in search
        predecesssor = {source: None}
        successors = {target: None}

        # initialize borders, start with forward
        forward_border = [source]
        backward_border = [target]

        while forward_border and backward_border:
            if len(forward_border) <= len(backward_border):
                current_level = forward_border
                forward_border = []
                for v in current_level:
                    for w in G_succ[v]:
                        if w not in predecesssor:
                            forward_border.append(w)
                            predecesssor[w] = v
                        if w in successors:  # path found
                            return predecesssor, successors, w
            else:
                current_level = backward_border
                backward_border = []
                for v in current_level:
                    for w in G_pred[v]:
                        if w not in successors:
                            successors[w] = v
                            backward_border.append(w)
                        if w in predecesssor:  # found path
                            return predecesssor, successors, w

        return np.inf

    def spanning_tree(self, source):
        visited = dict()#is the list containing the nodes of the shortest path between the source and the target
        visited[source] = 'null'
        to_visit = deque([source])
        while(to_visit):
            visiting = to_visit.pop()
            vicini = set(self.G.neighbors(visiting))
            yield {vicino : visiting for vicino in vicini if vicino not in visited}
            visited.update({vicino : visiting for vicino in vicini if vicino not in visited})
            to_visit.extendleft(vicini)

    class Generator:
        def __init__(self, gen):
            self.gen = gen

        def __iter__(self):
            self.value = yield from self.gen

    def wrapper(self, source, destinations):
        def depth(st, source, dest, deep):
            for i in st:
                if dest == source:
                    yield dest
                    global var
                    var = deep
                    return var
                if dest in i:
                    yield dest
                    yield from depth(self.spanning_tree(self.G, source), 
                                     source, i[dest], deep+1)
                    return var

        st = self.spanning_tree(self.G, source)
        gen = []
        for dest in destinations:
            gen.append(self.Generator(depth(st, source ,dest,0)))
        return gen

    def multithread_engine(self, *args):
        f = open(args[0]+'.json', 'w') #this will be the output jsonfile
        # if the current category is the input category, simply put -1 inside the file and stop the thread
        if args[0] == self.input_category:
            json.dump({self.input_category: -1}, f)
            f.close()
            return
        """
         This will contains the median scaled by a value 
         that is proportional to the numbers of infinites inside the procedure 
         that builds the collections of shortest paths from C0 to Ci.
        """
        data = {}
        infs = 0
        paths = []
        
        """ For each node in the input category and for each node in the Ci category. """
        for nodec0 in self.categories[self.input_category]:
            for nodec1 in self.categories[args[0]]:
                """ compute the shortest path with the two-sided bfs that simulate the dijkstra algorithm for sp """
                sp = self.shortest_path_bidir(nodec0, nodec1)
                """ 
                    if there's no path you increment the numbers of infinites 
                    instead of placing the np.inf on the collection of path lengths
                    if everything was good, 
                    you simply add the length of the path to the main collection,
                    the length of the path is the length of the list in output from the bfs algorithm minus one.
                """
                if sp is np.inf:
                    infs += 1
                elif sp is not None:
                       paths.append( len(sp)-1 )

        
        data[args[0]] = np.median(paths) + ((infs**.5)*np.log(infs+1))
        json.dump(data, f)
        f.close()
        return

   

    def scheduler(self):
        
        """
            Creating a scheduler function to check the number of threads and assigning each thread to do the computation for each category
            and combine the results for each task.
        """
        virtuals = cpu_count()
        for i in range(0,len(self.categories), virtuals-1): #scroll the categories in groups of virtuals-1 
            synchronization_stack = [] # is a data structure for save the started threads and control them later on.
            """
            Pick 'virtuals' categories and if it doesen't exceed the number of categories 
            you start a new thread and attach to it the function defined before with parameter:
                   
                - The actual category you are performing the shortest path algorithm bidibi bodibi bu.
                
            """
            for j in range(virtuals):
                if(i+j < len(self.categories)):
                    t = Thread(target=self.multithread_engine, 
                               args=(list(self.categories.keys())[i+j], 'null'))
                    t.start()
                    synchronization_stack.append(t)
            for thread in synchronization_stack:
                thread.join()
                
        """ you have all the results. The only thing that remains to do is to combine the results provided by the concurrency. """
        recombinator = self.combine()
        self.block_ranking = recombinator
        fptr = open('dropthebayes.json', 'w')
        json.dump(recombinator, fptr)
        fptr.close()
        return recombinator

    def combine(self):
        values = {}
        for cat in self.categories:
            f = open(cat+'.json', 'r')
            values.update(json.load(f))
            f.close()
        return sorted(values.items(), key=lambda kv: kv[1])

    def cat_builder(self):
        block_ranking = [elem[0] for elem in json.load(open('dropthebayes.json', 'r'))]
        visited = set()
        for supcategory in block_ranking:
            bigset = set()
            visited.add(supcategory)
            for subcategory in block_ranking:
                if subcategory in visited:
                    continue
                else:
                    bigset = bigset.union(set(self.categories[subcategory]).intersection(self.categories[supcategory]))
                        
            for subcategory_tmp_rmv in block_ranking:
                if subcategory_tmp_rmv in visited:
                    continue
                else:
                    self.categories[subcategory_tmp_rmv] = set(self.categories[subcategory_tmp_rmv]).difference(bigset)
                
    def in_degree(self, G):
        indegre = {}
        """
        init dei pesi
        """
        for node in G.nodes():
            indegre[node] = 0
        for edge in G.edges():
            indegre[edge[1]] += G[edge[0]][edge[1]]['w']
        return indegre
    
    
    def pagerank(self):
        """
        TODO:  SOSTITUIRE F CON IL BLOCK RANKING.
        
        """
        first_subgraph = self.G.subgraph(nodes=self.categories[self.block_ranking[0][0]])
        for edge in first_subgraph.edges():
            first_subgraph[edge[0]][edge[1]]['w'] = 1
        scores = self.in_degree(first_subgraph)
                
        for i in range(1, len(self.block_ranking)):
            second_subgraph = nx.DiGraph(first_subgraph)
            second_subgraph.add_edges_from(self.G.subgraph(self.categories[self.block_ranking[i][0]]).edges())
            for edge in second_subgraph.edges():
                if edge[1] in self.categories[self.block_ranking[i][0]]:
                    if edge[0] in scores:
                        second_subgraph[edge[0]][edge[1]]['w'] = scores[edge[0]]
                    else:         
                        second_subgraph[edge[0]][edge[1]]['w'] = 1
                
        scores = self.in_degree(second_subgraph)
        first_subgraph = nx.DiGraph(second_subgraph)
        return scores