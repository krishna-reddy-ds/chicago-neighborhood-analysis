import os
import warnings
import pandas as pd
import networkx as nx

warnings.filterwarnings('ignore')

from config import CAS, CA_TRACTS
from data_fetcher import fetch_ca_blockgroups
from features import compute_features, create_temporal_analysis
from network import build_cross_ca_network, analyze_network
from communities import detect_communities_louvain, detect_communities_leiden
from visualizations import (
    create_temporal_viz,
    create_community_comparison,
    create_network_geographic,
    create_feature_correlations,
    create_ca_profiles,
    create_interactive_map
)

def main():
    print("="*60)
    print("Chicago Community Boundaries Network Analysis")
    print("="*60)

    os.makedirs("final_figs", exist_ok=True)

    # Fetch 2022 data
    print("\n[1/6] Fetching 2022 data...")
    all_dfs_2022 = []
    for ca_id, ca_name in CAS.items():
        print(f"  {ca_name}...", end=" ")
        tracts = CA_TRACTS.get(ca_id, [])
        if tracts:
            df_ca = fetch_ca_blockgroups(ca_id, tracts, year="2022")
            if not df_ca.empty:
                all_dfs_2022.append(df_ca)
                print(f"{len(df_ca)} block groups")

    df_2022 = pd.concat(all_dfs_2022, ignore_index=True)
    print(f"  Total: {len(df_2022)} block groups")

    # Fetch 2014 data
    print("\n[2/6] Fetching 2014 data...")
    all_dfs_2014 = []
    for ca_id, ca_name in CAS.items():
        print(f"  {ca_name}...", end=" ")
        tracts = CA_TRACTS.get(ca_id, [])
        if tracts:
            df_ca = fetch_ca_blockgroups(ca_id, tracts, year="2014")
            if not df_ca.empty:
                all_dfs_2014.append(df_ca)
                print(f"{len(df_ca)} block groups")

    df_2014 = pd.concat(all_dfs_2014, ignore_index=True)
    print(f"  Total: {len(df_2014)} block groups")

    # Compute features
    print("\n[3/6] Computing features...")
    df_2022 = compute_features(df_2022)
    df_2014 = compute_features(df_2014)

    feature_cols = [
        'share_white', 'share_black', 'share_hispanic',
        'share_ba_plus', 'renter_share', 'homeownership_rate',
        'med_income_log', 'med_rent_log',
        'foreign_born_share', 'vacancy_rate', 'walk_to_work_share'
    ]

    # Build network
    print("\n[4/6] Building network...")
    G_2022, sim_matrix, valid_cols, X_scaled = build_cross_ca_network(df_2022, feature_cols, k=10)
    print(f"  {G_2022.number_of_nodes()} nodes, {G_2022.number_of_edges()} edges")

    stats = analyze_network(G_2022, df_2022)
    print(f"  Cross-CA edges: {stats['cross_ca_percentage']:.1f}%")

    # Detect communities
    print("\n[5/6] Detecting communities...")
    communities_louvain = detect_communities_louvain(G_2022)
    print(f"  Louvain: {len(communities_louvain[0])} communities, Q={communities_louvain[1]:.3f}")

    communities_leiden = detect_communities_leiden(G_2022)
    if communities_leiden[0] is not None:
        print(f"  Leiden: {len(communities_leiden[0])} communities, Q={communities_leiden[1]:.3f}")

    # Temporal analysis
    temporal_comparison = create_temporal_analysis(df_2014, df_2022)

    # Generate visualizations
    print("\n[6/6] Generating visualizations...")
    create_temporal_viz(temporal_comparison)
    print("  ✓ 01_temporal_analysis.png")

    create_community_comparison(G_2022, communities_louvain, communities_leiden)
    print("  ✓ 02_community_comparison.png")

    create_network_geographic(G_2022, df_2022, stats)
    print("  ✓ 03_network_geographic.png")

    create_feature_correlations(df_2022, valid_cols)
    print("  ✓ 04_feature_correlations.png")

    create_ca_profiles(df_2022)
    print("  ✓ 05_ca_profiles.png")

    create_interactive_map(df_2022, communities_louvain[2])
    print("  ✓ interactive_map.html")

    # Save data
    df_2022.to_csv('final_figs/data_2022.csv', index=False)
    df_2014.to_csv('final_figs/data_2014.csv', index=False)
    nx.write_gexf(G_2022, 'final_figs/network_2022.gexf')

    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)
    print(f"\nKey findings:")
    print(f"  • {stats['cross_ca_percentage']:.1f}% of connections cross official boundaries")
    print(f"  • {len(communities_louvain[0])} communities detected (Q={communities_louvain[1]:.3f})")
    print(f"  • Results saved to final_figs/")
    print("="*60)

if __name__ == "__main__":
    main()
