import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from matplotlib.patches import Patch

try:
    import folium
    HAS_FOLIUM = True
except:
    HAS_FOLIUM = False

from config import CA_COORDS

def create_temporal_viz(temporal_comparison, output_dir='final_figs'):
    if not temporal_comparison or len(temporal_comparison) == 0:
        return

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Temporal Changes: 2014 vs 2022', fontsize=16, fontweight='bold')

    metrics_plot = list(temporal_comparison.keys())[:6]
    while len(metrics_plot) < 6:
        metrics_plot.append(None)

    for idx in range(6):
        ax = axes[idx // 3, idx % 3]

        if idx < len(list(temporal_comparison.keys())) and metrics_plot[idx] is not None:
            metric = metrics_plot[idx]
            data = temporal_comparison[metric]

            years = ['2014', '2022']
            values = [data['2014'], data['2022']]
            change = data['change_pct']

            bars = ax.bar(years, values, color=['#3498db', '#e74c3c'])
            ax.set_title(f'{metric.replace("_", " ").title()}\n({change:+.1f}% change)',
                        fontweight='bold')
            ax.set_ylabel('Value')

            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.3f}', ha='center', va='bottom', fontsize=9)
        else:
            ax.axis('off')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_temporal_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_community_comparison(G_2022, communities_louvain, communities_leiden, output_dir='final_figs'):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Community Detection: Louvain vs Leiden', fontsize=16, fontweight='bold')

    pos = nx.spring_layout(G_2022, k=0.5, iterations=50, seed=42)

    comms_louvain, mod_louvain, node_to_comm_louvain = communities_louvain
    colors_louvain = [node_to_comm_louvain.get(node, 0) for node in G_2022.nodes()]

    nx.draw_networkx_nodes(G_2022, pos, node_color=colors_louvain,
                          node_size=50, alpha=0.7, cmap='tab10', ax=axes[0])
    nx.draw_networkx_edges(G_2022, pos, alpha=0.1, width=0.5, ax=axes[0])
    axes[0].set_title(f'Louvain Algorithm\n{len(comms_louvain)} communities, Q={mod_louvain:.3f}',
                     fontweight='bold')
    axes[0].axis('off')

    if communities_leiden[0] is not None:
        comms_leiden, mod_leiden, node_to_comm_leiden = communities_leiden
        colors_leiden = [node_to_comm_leiden.get(node, 0) for node in G_2022.nodes()]

        nx.draw_networkx_nodes(G_2022, pos, node_color=colors_leiden,
                              node_size=50, alpha=0.7, cmap='tab10', ax=axes[1])
        nx.draw_networkx_edges(G_2022, pos, alpha=0.1, width=0.5, ax=axes[1])
        axes[1].set_title(f'Leiden Algorithm\n{len(comms_leiden)} communities, Q={mod_leiden:.3f}',
                         fontweight='bold')
        axes[1].axis('off')
    else:
        axes[1].text(0.5, 0.5, 'Leiden algorithm\nnot available',
                    ha='center', va='center', transform=axes[1].transAxes, fontsize=14)
        axes[1].axis('off')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_community_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_network_geographic(G_2022, df_2022, stats, output_dir='final_figs'):
    fig, ax = plt.subplots(figsize=(12, 10))

    pos = nx.spring_layout(G_2022, k=0.5, iterations=50, seed=42)

    ca_names = sorted(df_2022['ca_name'].unique())
    ca_colors = {ca: plt.cm.Set2(i) for i, ca in enumerate(ca_names)}
    node_colors = [ca_colors[G_2022.nodes[node]['ca_name']] for node in G_2022.nodes()]

    nx.draw_networkx_nodes(G_2022, pos, node_color=node_colors,
                          node_size=50, alpha=0.7, ax=ax)

    cross_edges = [(u,v) for u,v in G_2022.edges()
                   if G_2022.nodes[u]['ca_id'] != G_2022.nodes[v]['ca_id']]
    nx.draw_networkx_edges(G_2022, pos, edgelist=cross_edges,
                          edge_color='red', alpha=0.3, width=1.0, ax=ax)

    within_edges = [(u,v) for u,v in G_2022.edges()
                    if G_2022.nodes[u]['ca_id'] == G_2022.nodes[v]['ca_id']]
    nx.draw_networkx_edges(G_2022, pos, edgelist=within_edges,
                          edge_color='gray', alpha=0.1, width=0.3, ax=ax)

    legend_elements = [Patch(facecolor=ca_colors[ca], label=ca) for ca in ca_names]
    legend_elements.append(Patch(facecolor='red', alpha=0.5, label='Cross-CA connections'))
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

    ax.set_title(f'Cross-City Network Structure (2022)\n{stats["cross_ca_percentage"]:.1f}% of connections cross official boundaries',
                fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_network_geographic.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_feature_correlations(df_2022, valid_cols, output_dir='final_figs'):
    fig, ax = plt.subplots(figsize=(10, 8))

    feature_data = df_2022[valid_cols].copy()
    for col in valid_cols:
        feature_data[col] = feature_data[col].fillna(feature_data[col].median())

    corr_matrix = feature_data.corr()

    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_feature_correlations.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_ca_profiles(df_2022, output_dir='final_figs'):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Socioeconomic Profiles by Community Area (2022)', fontsize=16, fontweight='bold')

    metrics = [
        ('med_income', 'Median Household Income ($)'),
        ('share_ba_plus', 'Bachelor\'s Degree or Higher (%)'),
        ('homeownership_rate', 'Homeownership Rate (%)'),
        ('vacancy_rate', 'Housing Vacancy Rate (%)')
    ]

    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]

        ca_data = df_2022.groupby('ca_name')[metric].median().sort_values(ascending=False)

        bars = ax.barh(range(len(ca_data)), ca_data.values,
                      color=plt.cm.Set2(range(len(ca_data))))
        ax.set_yticks(range(len(ca_data)))
        ax.set_yticklabels(ca_data.index)
        ax.set_xlabel('Value')
        ax.set_title(title, fontweight='bold')

        for i, (bar, val) in enumerate(zip(bars, ca_data.values)):
            if metric == 'med_income':
                label = f'${val:,.0f}'
            elif 'rate' in metric or 'share' in metric:
                label = f'{val*100:.1f}%'
            else:
                label = f'{val:.2f}'

            ax.text(val, bar.get_y() + bar.get_height()/2.,
                   f'  {label}', ha='left', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_ca_profiles.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_interactive_map(df, communities_dict, output_file='final_figs/interactive_map.html'):
    if not HAS_FOLIUM:
        return

    m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, tiles='OpenStreetMap')

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
              'lightred', 'beige', 'darkblue', 'darkgreen']

    for idx, row in df.iterrows():
        if idx in communities_dict:
            comm_id = communities_dict[idx]
            color = colors[comm_id % len(colors)]

            ca_id = row['ca_id']
            if ca_id in CA_COORDS:
                lat, lon = CA_COORDS[ca_id]
                lat += np.random.randn() * 0.01
                lon += np.random.randn() * 0.01

                popup_text = f"""
                <b>Block Group:</b> {row['geoid_bg']}<br>
                <b>CA:</b> {row['ca_name']}<br>
                <b>Community:</b> {comm_id}<br>
                <b>Pop:</b> {row.get('B01003_001E', 'N/A')}<br>
                <b>Med Income:</b> ${row.get('med_income', 0):,.0f}
                """

                folium.CircleMarker(
                    location=[lat, lon],
                    radius=5,
                    popup=folium.Popup(popup_text, max_width=200),
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.6
                ).add_to(m)

    m.save(output_file)
