from typing import Annotated

from fastapi import HTTPException, Query
from rdflib import Namespace, URIRef

from kitchen_chef_server.app import app, g
from kitchen_chef_server.factories.IngredientFactory import IngredientFactory
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
            initBindings[f"ingredientFood{i}"] = URIRef(food_ingredient)
            pass

    results = g.query(query, initBindings=initBindings)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes = []
    for row in results:
        ingredients = IngredientFactory.from_strings(
            row.ingredientIds,
            row.ingredientNames,
            row.ingredientFoods,
            row.ingredientQuantities,
            row.ingredientUnits,
        )
        recipe = Recipe(row.recipe, row.name, ingredients, row.instructions, row.category, row.thumbnail)
        recipes.append(recipe)

    return recipes


@app.get("/recipe")
async def get_recipe(recipe_identifier: str):
    query = """
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT ?recipe ?name ?category ?instructions ?thumbnail
            (group_concat(?ingredient; separator="|-|") AS ?ingredientIds)
            (group_concat(?ingredientFood; separator="|-|") AS ?ingredientFoods)
            (group_concat(?ingredientName; separator="|-|") AS ?ingredientNames)
            (group_concat(?ingredientQuantity; separator="|-|") AS ?ingredientQuantities)
            (group_concat(?ingredientUnit; separator="|-|") AS ?ingredientUnits)
    WHERE {
        ?recipe :name ?name ;
                :hasIngredient ?ingredient .
        OPTIONAL { ?recipe :recipeCategory ?category . }
        OPTIONAL { ?recipe :instructions ?instructions . }
        OPTIONAL { ?recipe :hasThumbnail ?thumbnail . }

        ?ingredient :name ?ingredientName .
        OPTIONAL {{ ?ingredient :food ?ingredientFood . }}
        OPTIONAL {{ ?ingredient :quantity ?ingredientQuantity . }}
        OPTIONAL {{ ?ingredient :unit ?ingredientUnit . }}

        FILTER(?recipe = ?uri)
    } GROUP BY ?recipe
    """

    results = g.query(
        query,
        initBindings={
            "uri": URIRef(recipe_identifier),
        },
    )

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for row in results:
        ingredients = IngredientFactory.from_strings(
            row.ingredientIds,
            row.ingredientNames,
            row.ingredientFoods,
            row.ingredientQuantities,
            row.ingredientUnits,
        )
        return Recipe(row.recipe, row.name, ingredients, row.instructions, row.category, row.thumbnail)
