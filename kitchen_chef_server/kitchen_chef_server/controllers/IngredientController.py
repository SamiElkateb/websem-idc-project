from typing import Annotated
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from rdflib import Graph, Namespace, URIRef

from kitchen_chef_server.app import app, g
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

    results = g.query(
        query,
    )

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    foods = {}
    for row in results:
        food = Food(row.food, row.thumbnail, row.enLabel, row.frLabel)
        foods[row.food] = food
    return list(foods.values())


@app.get("/test")
async def get_test():
    query = """
    prefix : <http://project-kitchenchef.fr/schema#>

    select * where {
      ?x a :ArachisRecipe
    }
    """

    results = g.query(
        query,
    )

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for row in results:
        print("result row", row.x)
