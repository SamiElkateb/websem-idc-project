from fastapi import FastAPI

from kitchen_chef_server.utils.load_graph import load_graph

app = FastAPI()

g = load_graph("./data")
