from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from kitchen_chef_server.conf import CORESE_URL
from kitchen_chef_server.utils.load_graph import load_graph
from kitchen_chef_server.utils.read_query import read_query
from kitchen_chef_server.utils.sparql_service_update import sparql_service_update
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

# sparql_service_update(CORESE_URL, read_query("./kitchen_chef_server/sparql/inserts/conversion_ratios.rq"))
# sparql_service_update(CORESE_URL, read_query("./kitchen_chef_server/sparql/inserts/conversion.rq"))
# sparql_service_update(CORESE_URL, read_query("./kitchen_chef_server/sparql/entailment/complementary_recipe.rq"))

print("ALL entailment done")
