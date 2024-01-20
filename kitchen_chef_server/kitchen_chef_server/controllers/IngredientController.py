from typing import Annotated
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from kitchen_chef_server.conf import CORESE_URL
from kitchen_chef_server.utils.corese_query import corese_query
from kitchen_chef_server.utils.read_query import read_query
from kitchen_chef_server.utils.sparql_service_update import sparql_service_update
from rdflib import Graph, Namespace, URIRef

from kitchen_chef_server.app import app
from kitchen_chef_server.models.Food import Food

RECIPES = Namespace("http://project-kitchenchef.fr/recipes/data#")
FOODS = Namespace("http://project-kitchenchef.fr/food/data#")


@app.get("/ingredients")  # TODO: JSON-LD
async def get_ingredients():
    print("ingredients")
    query = """
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT DISTINCT ?food ?frLabel ?enLabel ?thumbnail WHERE {
           ?food a :Food ;
                 :hasThumbnail ?thumbnail ;
                 rdfs:label ?frLabel ;
                 rdfs:label ?enLabel .
           FILTER (LANG(?frLabel) = "fr")
           FILTER (LANG(?enLabel) = "en")
    }
    """

    results = corese_query(query)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    foods = {}
    for index, row in results:
        food = Food(row["food"], row["thumbnail"], row["enLabel"], row["frLabel"])
        foods[row.food] = food
    return list(foods.values())


@app.get("/test")
async def get_test():
    query = """
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT DISTINCT ?recipe ?name
    WHERE {{
        ?recipe a :VeganRecipe ;
                :name ?name .
    }} GROUP BY ?recipe
    """

    results = corese_query(query)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")
    recipes = []

    recipes = []
    for index, row in results:
        print("results row", row["name"])
        print("result row", row.name)
        recipes.append(row["name"])
    return recipes


@app.get("/prepare")
async def prepare():
    sparql_service_update(CORESE_URL, read_query("./kitchen_chef_server/sparql/inserts/conversion_ratios.rq"))
    sparql_service_update(CORESE_URL, read_query("./kitchen_chef_server/sparql/inserts/conversion.rq"))
    sparql_service_update(CORESE_URL, read_query("./kitchen_chef_server/sparql/entailment/complementary_recipe.rq"))
    return "Done"
