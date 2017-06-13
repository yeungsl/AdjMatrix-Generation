#!/usr/bin/env python
#coding:utf-8
"""
Author: Sailung Yeung <yeungsl@bu.edu>
"""
import os
import sys
import argparse
import networkx as nx
import Conditional_Topology_MAIN as CTM
from external_tools.community_louvain import generate_dendrogram, partition_at_level

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, default="facebook", help="Datasets Choose")
    parser.add_argument("--noise", type=int, default=10, help="ignor the community that is has size smaller than this nubmer")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    filename = args.filename
    noise = args.noise
    path = os.path.join('data', filename, '')
    graph = CTM.generate_graph(path, filename, -1)
    print("got graph from CTM with", len(graph.nodes()), "nodes and", len(graph.edges()),"edges......")
    dendrogram = generate_dendrogram(graph)
    print("length of the dendrogram generated is", len(dendrogram), "we are using the best layer by defealt")
    best = dendrogram[len(dendrogram) - 1]
    communities = {}

    for node in best.keys():
        com_num = best[node]
        if com_num not in communities.keys():
            communities[com_num] = [node]
        else:
            communities[com_num].append(node)

    for com_num in communities.keys():
        if len(communities[com_num]) >= noise:
            com = graph.subgraph(communities[com_num])
