import numpy as np
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

def build_cross_ca_network(df, feature_cols, k=10):
    X = df[feature_cols].copy()

    valid_cols = []
    for col in feature_cols:
        if X[col].notna().sum() > 0:
            valid_cols.append(col)

    X = X[valid_cols].copy()

    for col in valid_cols:
        median_val = X[col].median()
        if np.isnan(median_val):
            median_val = 0.0
        X[col] = X[col].fillna(median_val)

    X_array = X.to_numpy()
    X_array = np.nan_to_num(X_array, nan=0.0, posinf=0.0, neginf=0.0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_array)
    X_scaled = np.nan_to_num(X_scaled, nan=0.0, posinf=0.0, neginf=0.0)

    sim_matrix = cosine_similarity(X_scaled)

    G = nx.Graph()
    n_nodes = len(df)

    for i in range(n_nodes):
        G.add_node(i,
                  geoid=df.iloc[i]['geoid_bg'],
                  ca_id=df.iloc[i]['ca_id'],
                  ca_name=df.iloc[i]['ca_name'],
                  year=df.iloc[i].get('year', '2022'))

    for i in range(n_nodes):
        neighbors = np.argsort(sim_matrix[i])[::-1][1:k+1]
        for j in neighbors:
            if i < j:
                G.add_edge(i, j, weight=float(sim_matrix[i,j]))

    return G, sim_matrix, valid_cols, X_scaled

def analyze_network(G, df):
    stats = {
        'total_nodes': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'density': nx.density(G)
    }

    within_ca = 0
    cross_ca = 0

    for u, v in G.edges():
        ca_u = G.nodes[u]['ca_id']
        ca_v = G.nodes[v]['ca_id']
        if ca_u == ca_v:
            within_ca += 1
        else:
            cross_ca += 1

    stats['within_ca_edges'] = within_ca
    stats['cross_ca_edges'] = cross_ca
    stats['cross_ca_percentage'] = 100 * cross_ca / max(within_ca + cross_ca, 1)

    return stats
