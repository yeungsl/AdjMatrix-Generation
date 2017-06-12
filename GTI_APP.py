import os
import sys
import Conditional_Topology_MAIN as CTM
from external_tools.community_louvain import generate_dendrogram, partition_at_level

if __name__ == "__main__":
    filename = sys.argv[1]
    path = os.path.join('data', filename, '')
    graph = CTM.generate_graph(path, filename, -1)
    print("got graph from CTM with", len(graph.nodes()), "nodes and", len(graph.edges()),"edges......")
    dendrogram = generate_dendrogram(graph)
    print("length of the dendrogram generated is", len(dendrogram))
    for level in range(len(dendrogram)):
        stats = dict()
        cur_layer = partition_at_level(dendrogram, level)
        for node in cur_layer.keys():
            if cur_layer[node] in stats.keys():
                stats[cur_layer[node]] += 1
            else:
                stats[cur_layer[node]] = 1

        avg = len(graph.nodes()) / len(stats.keys())
        print("for layer", level, "we have", len(stats.keys()), "and avg", avg, "that has stats", stats)
        if avg >= 4500 and avg <= 5000:
            print("found the level that has around 5000 nodes in one community")
            print("the partition is at level", level, "that has stats", stats)
            break
