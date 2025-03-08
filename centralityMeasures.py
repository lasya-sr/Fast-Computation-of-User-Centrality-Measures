# -*- coding: utf-8 -*-
"""47336991.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GZzamP09GOuZjMbSPHcGuPr2ePurFrud
"""

import numpy as np

def create_graph(filename):
  # Initializing an empty dictionary to represent graph
  graph = {}
  filename = 'data.txt'

  # Open the data.txt file in read mode
  with open(filename, 'r') as file:
    # Iterating over each line of the file
    for lines in file:
      # Stripping the whitespace characters and spliting the line to form a list
      li = lines.strip().split()
      # Extracting nodes from the list
      node1 = li[0]
      node2 = li[1]

      # Checking if the node1 is already in the graph
      if node1 not in graph:
        graph[node1] = [node2]  # if not, adding node1 to the graph with node2 as its neighbour
      else:
        graph[node1].append(node2)  # if node1 already exists in the graph, append node2 to its list of neighbours

      # Check if node2 is already in the graph
      if node2 not in graph:
        graph[node2] = [node1]  # if not, adding node2 to the graph with node1 as its neighbour
      else:
        graph[node2].append(node1) # if node2 already exists in the graph, append node1 to its list of neighbours


  return graph

def betweenness_centrality(adj_list):
    # Initializing the betweenness dictionary bet_dict with edges and setting those values to 0
    bet_dict = {edge: 0 for edge in adj_list.keys()}

    # Iterating over each node of the graph as a source node for shortest paths
    for source in adj_list.keys():
        visited_nodes = []  # Visited nodes list
        pre_node = {} # Predecessor nodes
        len_of_sp = {} # Length of the shortest paths from source node

        for curr_node in adj_list.keys():
            pre_node[curr_node] = []
        no_of_sp = {curr_node: 0 for curr_node in adj_list}
        no_of_sp[source] = 1.0 # Shortest path count for source node
        len_of_sp[source] = 0 # Length of shortest path for source node
        queue = [source] # Creating a queue for BFS with source node

        # Performing BFS to find shortest paths from source node
        while queue:
            curr_node = queue.pop(0) # Dequeue the current node
            visited_nodes.append(curr_node) # Adding current node to the visited node list
            len_sourceTocurr_node = len_of_sp[curr_node] # len_sourceTocurr_node is the shortest path length to current node
            curr_node_sp = no_of_sp[curr_node] # Shortest path count for current node

            # Iterating the neighbours of current node
            for neighbour_node in adj_list[curr_node]:
                if neighbour_node not in len_of_sp:  # If the neighbour node not in visited
                    queue.append(neighbour_node)  # Enqueuing the neighbour node
                    len_of_sp[neighbour_node] = len_sourceTocurr_node + 1  # Updating the shortest path length
                if len_of_sp[neighbour_node] == len_sourceTocurr_node + 1: # If the shortest path is found
                    no_of_sp[neighbour_node] += curr_node_sp  # Incrementing the shortest path count
                    pre_node[neighbour_node].append(curr_node)  # Updating predecessor nodes

        # Accumulating deppendency scores using reverese BFS traversal
        delta = {curr_node: 0 for curr_node in visited_nodes}  #Initializing dependency scores
        while visited_nodes:
            neighbour_node = visited_nodes.pop()  # Pop the visited node
            coeff = (1 + delta[neighbour_node]) / no_of_sp[neighbour_node]  # Computing the coefficient
            for curr_node in pre_node[neighbour_node]:  #Updating the dependency scores for predecessors
                c_each = no_of_sp[curr_node] * coeff  # c_each is the contribution of each node
                delta[curr_node] += c_each
            if neighbour_node != source:  # Excluding the aource node from betweenness calculation
                bet_dict[neighbour_node] += delta[neighbour_node]  # Updating the betweenness score
    # Returns the betweenness score for each node
    return bet_dict



def pagerank_centrality(graph, alpha, beta):
    # Constructing the adjacency matrix
    l = len(graph)
    node_ids = sorted(list(graph.keys()))
    # Initializing the adjacency matrix, M with zeros
    M = np.zeros((l, l))

    # Populating the adjacency matrix
    for i in range(len(node_ids)):
        for j in range(len(node_ids)):
            if node_ids[j] in graph[node_ids[i]]:
                M[i][j] = 1

    # Constructing the degree matrix
    D = np.diag(M.sum(axis=1))

    # Power iteration to calculate PageRank vector
    threshold = 1e-6   # threshold indicates the convergence threshold
    c = 0      # c is the counter for iteration initialized to 0
    prev_pageRank = np.zeros(l)  # Intitializing the previous pageRank vector
    pageRank = np.ones(l) / l   # Initializing the current pageRank vector
    while np.sum(np.abs(prev_pageRank-pageRank)) > threshold:
        if c < 9:  # Limiiting the number of iterations to avoid infinite loop
            c = c + 1
        prev_pageRank = pageRank # Updating previous pageRank vector
        pageRank = alpha * M.T @ np.linalg.inv(D) @ pageRank + beta  * np.ones(l) # Calculating the pageRank using the pageRank formula
        pageRank = pageRank / np.sum(np.abs(pageRank))  # Normalizing the pageRank vector

    # Converting the pageRank vector to dictionary format
    pageRank = dict(zip([i for i in range(len(pageRank))], pageRank))

    # Returning the pageRank centrality scores for each node
    return pageRank



def main():
  # Calculating Betweenness Centrality scores of the graph by calling betweenness_centrality function
  centrality_scores = betweenness_centrality(graph)
  # Sorting the nodes based on their centrality scores in descending order
  sorted_nodes = sorted(centrality_scores.items(), key=lambda x: x[1], reverse=True)
  # Initializing the output1 string for top 10 nodes
  output1 = ""
  # Extracting the top 10 nodes and formating them into output1 string
  for node, centrality in sorted_nodes[:10]:
      output1 += f"{node} "

  # Calculating the PageRank Centrality scores of the graph by calling pagerank_centrality funtion
  # alpha=0.85 and beta=0.15
  pagerank_results = pagerank_centrality(graph, 0.85, 0.15)
  # Sorting the nodes based on their PageRank centrality scores in descending order
  sorted_nodes_pr = sorted(pagerank_results.items(), key=lambda x: x[1], reverse=True)
  # Initializing the output2 string for top 10 nodes
  output2 = ""
  # Extracting the top 10 nodes and formating them into output2 string
  for node, centrality in sorted_nodes_pr[:10]:
      output2 += f"{node} "

  # Write the output strings to the "47336991.txt" file
  with open("47336991.txt", "w") as output_file:
    output_file.write(output1.strip() + "\n")
    output_file.write(output2.strip() )

if __name__ == "__main__":
    graph = create_graph('data.txt')
    main()

