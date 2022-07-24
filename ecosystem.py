import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import math
import networkx as nx
from pyvis.network import Network

from networkx.algorithms.community import greedy_modularity_communities

@st.cache()
def load_edges():
	edges = pd.read_csv("che-server.csv")
	return edges

def create_ecosystem_network(edges, link_filter=1000):
	# Create an undirected network graph
    G = nx.Graph()

    # Each contributor is a network node
    contributors = set(edges["from"]).union(set(edges["to"]))
    G.add_nodes_from(contributors)

	# Remove negligible edges based on a filter
    for u, v, weight in edges.itertuples(index=False):
        if weight >= link_filter:
            G.add_edge(u, v, weight=weight)

    # Remove isolates (nodes without any neighbors)
    isolates = set(nx.isolates(G))
    G.remove_nodes_from(isolates)

    # Change size of nodes based on degree
    degrees = dict(nx.degree(G))
    max_degree = max(degrees.values())
    for node, degree in degrees.items():
        G.nodes[node]['size'] = 15 + 10 * math.log10(degree/max_degree)

    # Change color of nodes based on name
    # TODO: Modify this to change the colors of the contributors
    for node, data in G.nodes(data=True):
        if node.endswith("codenvy.com"):
            data['color'] = '#00ee00'   # green
        elif node.endswith("redhat.com"):
            data['color'] = '#ee0000'   # red
        else:
            data['color'] = '#eeeeee'   # grey

    return G

def show_ecosystem_network(G):
	network = Network('600px', '600px')
	network.from_nx(G)
	network.show("ecosystem_network.html")
	with st.container():
		components.html(open("ecosystem_network.html", 'r', encoding='utf-8').read(), height=625)

def show_ecosystem_metrics(G):
    # TODO: Calculate and display networks metrics that allow you to understand the network,
    # such as the key actors, the key actors' roles, etc.
    pass

# app

st.sidebar.title("Ecosystem")

st.header("Edges")
st.markdown("""
    This is a list of all the edges in the ecosystem. Click on the column headers to sort.
""")
edges = load_edges()
st.dataframe(edges)

st.header("Ecosystem network")
st.markdown("""
    Visualize the ecosystem network. Experiment with the link filter to see how it affects the network.
""")

min_link_weight = st.sidebar.slider("Minimum link weight", min_value=0, max_value=10000, value=1000, step=50)
G = create_ecosystem_network(edges, link_filter=min_link_weight)
st.sidebar.write("{} nodes, {} edges".format(len(G.nodes), len(G.edges)))
show_ecosystem_network(G)

st.header("Metrics")
st.markdown("""
    Calculate and display metrics that allow you to understand the network.
""")
show_ecosystem_metrics(G)