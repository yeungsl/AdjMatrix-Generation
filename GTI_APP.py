#!/usr/bin/env python
#coding:utf-8
"""
Author: Sailung Yeung <yeungsl@bu.edu>
"""
import os, sys, argparse, pickle
import networkx as nx
import Conditional_Topology_MAIN as CTM
from external_tools.community_louvain import generate_dendrogram, partition_at_level

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, default="facebook", help="Datasets Choose")
    parser.add_argument("--noise", type=int, default=10, help="ignor the community that is has size smaller than this nubmer")
    return parser.parse_args()

def get_com_stats(graph):
    dendrogram = generate_dendrogram(graph)
    print("length of the dendrogram generated is", len(dendrogram), "we are using the best layer by defealt")
    best_part = partition_at_level(dendrogram, len(dendrogram)-1)
    communities = {}
    num = {}
    for node in best_part:
        com_num = best_part[node]
        if com_num not in communities.keys():
            communities[com_num] = [node]
            num[com_num] = 1
        else:
            communities[com_num].append(node)
            num[com_num] += 1

    return communities, num

def reduce_community(graph, noise):
    communities, num = get_com_stats(graph)
    exist, key = exist_invalied(num)
    print("These", key,"has size larger than 5000")
    #Base case for the recursion
    if not exist:
        graphs = []
        for com_num in communities.keys():
            if len(communities[com_num]) >= noise:
                g = graph.subgraph(communities[com_num])
                graphs.append(g)
        return graphs
    else:
        graphs = []
        for com_num in communities.keys():
            if len(communities[com_num]) >= noise:
                g = graph.subgraph(communities[com_num])
                if com_num in key:
                    graphs.extend(reduce_community(g, noise))
                else:
                    graphs.append(g)
        return graphs

def exist_invalied(num):
    key = []
    for k in num.keys():
        if num[k] >= 5000:
            key.append(k)
    if len(key) > 0:
        return True, key
    else:
        return False, key

if __name__ == "__main__":
    args = parse_args()
    filename = args.filename
    noise = args.noise
    Matsize = 0
    partition_info = []
    path = os.path.join('data', filename, '')
    graph = CTM.generate_graph(path, filename, -1)
    print("got graph from CTM with", len(graph.nodes()), "nodes and", len(graph.edges()),"edges......")
    graphs = reduce_community(graph, noise)


    index = 0
    map_file = open(path+"%s.id_map"%filename, '+w')
    metis_file = open(path+"%s_%d.metis_graph.part.%d"%(filename, Matsize, len(graphs)), '+w')
    for g in graphs:
        for node in g.nodes():
            map_file.write(str(node) + '\t' + str(index) + '\n')
            index += 1
            metis_file.write(str(graphs.index(g)) + '\n')

    max_size = CTM.generate_AdjMat(path, graph, Matsize, classNum=1)
    partition_info.append([len(graphs), max_size])

    pickle.dump(partition_info, open('%s_partition_info.pickle'%filename, '+wb'))
