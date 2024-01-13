from typing import Annotated
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from rdflib import Graph, Namespace, URIRef

from kitchen_chef_server.app import app, g
from kitchen_chef_server.models.Ingredient import Ingredient
from kitchen_chef_server.models.Recipe import Recipe
from kitchen_chef_server.sparql.queries.build_search_query import \
    build_search_query

RECIPES = Namespace("http://project-kitchenchef.fr/recipes/data#")
FOODS = Namespace("http://project-kitchenchef.fr/food/data#")


# TODO: query parameters: filter ingredients
@app.get("/recipes")
async def get_recipes(
    q_ingredients: Annotated[list[str] | None, Query()] = None,
    q_filters: Annotated[list[str] | None, Query()] = None,
):
    query = build_search_query(q_ingredients, q_filters)
    initBindings = {}
    if q_ingredients:
        for i, food_ingredient in enumerate(q_ingredients):
            initBindings[f"ingredientFood{i}"] = FOODS[food_ingredient]
            pass

    results = g.query(query, initBindings=initBindings)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes = {}
    for row in results:
        name = str(row.name)
        recipe_identifier = urlparse(row.recipe).fragment
        food_identifier = urlparse(row.ingredientFood).fragment
        ingredient_identifier = urlparse(row.ingredient).fragment
        ingredient = Ingredient(
            food_identifier,
            ingredient_identifier,
            row.ingredientName,
            row.ingredientQuantity,
            row.ingredientUnit,
        )
        instructions = str(row.instructions)
        category = str(row.category)

        recipe = recipes.get(recipe_identifier)

        if recipe:
            recipe.add_ingredient(ingredient)
        else:
            recipes[recipe_identifier] = Recipe(
                recipe_identifier, name, instructions, category
            )
            recipes[recipe_identifier].add_ingredient(ingredient)
    return list(recipes.values())


@app.get("/recipe")  # TODO: JSON-LD
async def get_recipe(recipe_identifier: str):
    query = """
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT ?name ?category ?ingredientFood ?ingredientName ?ingredientQuantity ?instructions ?ingredientUnit WHERE {
        ?recipe :name ?name ;
                :hasIngredient ?ingredient ;
                :instructions ?instructions ;
                :recipeCategory ?category .
        ?ingredient :food ?ingredientFood ;
                    :name ?ingredientName ;
                    :quantity ?ingredientQuantity ;
                    :unit ?ingredientUnit .
        FILTER(?recipe = ?uri)
    }
    """

    results = g.query(
        query,
        initBindings={
            "uri": RECIPES[recipe_identifier],
        },
    )

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes = {}
    for row in results:
        name = str(row.name)
        recipe_identifier = urlparse(row.recipe).fragment
        food_identifier = urlparse(row.ingredientFood).fragment
        ingredient_identifier = urlparse(row.ingredient).fragment
        ingredient = Ingredient(
            food_identifier,
            ingredient_identifier,
            row.ingredientName,
            row.ingredientQuantity,
            row.ingredientUnit,
        )
        instructions = str(row.instructions)
        category = str(row.category)

        recipe = recipes.get(recipe_identifier)

        if recipe:
            recipe.add_ingredient(ingredient)
        else:
            recipes[recipe_identifier] = Recipe(
                recipe_identifier, name, instructions, category
            )
            recipes[recipe_identifier].add_ingredient(ingredient)
    return list(recipes.values())[0]
