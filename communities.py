import networkx as nx

try:
    import leidenalg as la
    import igraph as ig
    HAS_LEIDEN = True
except:
    HAS_LEIDEN = False

def detect_communities_louvain(G):
    communities = list(nx.community.greedy_modularity_communities(G, weight='weight'))
    modularity = nx.community.modularity(G, communities, weight='weight')

    node_to_comm = {}
    for i, comm in enumerate(communities):
        for node in comm:
            node_to_comm[node] = i

    return communities, modularity, node_to_comm

def detect_communities_leiden(G):
    if not HAS_LEIDEN:
        return None, None, None

    try:
        edge_list = [(u, v, d['weight']) for u, v, d in G.edges(data=True)]
        g_ig = ig.Graph()
        g_ig.add_vertices(len(G.nodes()))
        g_ig.add_edges([(u, v) for u, v, _ in edge_list])
        g_ig.es['weight'] = [w for _, _, w in edge_list]

        partition = la.find_partition(g_ig, la.ModularityVertexPartition,
                                       weights='weight', n_iterations=-1)

        communities = [set(comm) for comm in partition]
        modularity = partition.modularity

        node_to_comm = {}
        for i, comm in enumerate(communities):
            for node in comm:
                node_to_comm[node] = i

        return communities, modularity, node_to_comm
    except Exception:
        return None, None, None
