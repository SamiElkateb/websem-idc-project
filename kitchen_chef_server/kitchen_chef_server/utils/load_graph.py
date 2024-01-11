import os
from rdflib import Graph, Namespace, URIRef


def load_graph(data_dir):
    g = Graph()
    for filename in os.listdir(data_dir):
        if filename.endswith(".ttl"):
            name = os.path.join(data_dir, filename)
            g.parse(name, format="turtle")
    return g
