from pathlib import Path
ROOT_DIR = Path('').resolve()
DATA_DIR = ROOT_DIR / 'data'
PARQUET_FILE = DATA_DIR / 'data.parquet'

import networkx as nx
import pandas as pd

# Read from Parquet file (much faster than CSV)
df = pd.read_parquet(PARQUET_FILE)
print("Create graph from Parquet file", PARQUET_FILE)
# Build the graph
G = nx.MultiDiGraph()

for _, row in df.iterrows():
    G.add_edge(
        row['question_user_id'],
        row['response_user_id'],
        question_id=row['question_id'],
        response_id=row['response_id']
    )

# Key contributor metrics
# 1. In-degree: Who answers the most questions?
in_degree = dict(G.in_degree())
top_answerers = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:10]
print("top_hubs", top_answerers)

# 2. PageRank: Who answers questions from important people?
pagerank = nx.pagerank(G)
top_by_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("top_by_pagerank", top_by_pagerank)

# 3. Betweenness: Who connects different communities?
betweenness = nx.betweenness_centrality(G)
top_connectors = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
print("top_connectors", top_connectors)

# 4. Hub score: Who asks questions that get good answers?
hits = nx.hits(G)
top_hubs = sorted(hits[0].items(), key=lambda x: x[1], reverse=True)[:10]
top_authorities = sorted(hits[1].items(), key=lambda x: x[1], reverse=True)[:10]
print("top_hubs", top_hubs)
print("top_authorities", top_authorities)
