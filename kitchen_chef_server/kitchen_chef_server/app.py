from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from kitchen_chef_server.utils.load_graph import load_graph
from kitchen_chef_server.utils.read_query import read_query
from owlrl import DeductiveClosure, OWLRL_Semantics

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

g = load_graph("./data")

g.update(read_query("./kitchen_chef_server/sparql/inserts/conversion_ratios.rq"))
g.update(read_query("./kitchen_chef_server/sparql/inserts/conversion.rq"))
DeductiveClosure(OWLRL_Semantics).expand(g)
g.update(read_query("./kitchen_chef_server/sparql/entailment/complementary_recipe.rq"))
