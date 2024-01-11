from fastapi import FastAPI, HTTPException
from kitchen_chef_server.models.Ingredient import Ingredient
from rdflib import Graph, Namespace, URIRef

from kitchen_chef_server.models.Recipe import Recipe
from kitchen_chef_server.utils.load_graph import load_graph

app = FastAPI()

g = load_graph("./data")

RECIPES = Namespace("http://project-kitchenchef.fr/recipes/data#")


# TODO: query parameters: filter ingredients
@app.get("/recipes")
async def get_recipes():
    return {"message": "Hello World"}


@app.get("/recipe")
async def get_recipe(recipe_uri: str):
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
            "uri": RECIPES[recipe_uri],
        },
    )

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    ingredients = []
    name, instructions, category = None, None, None
    for row in results:
        name = str(row.name)
        ingredients.append(Ingredient(row.ingredientFood, row.ingredientName, row.ingredientQuantity, row.ingredientUnit))
        instructions = str(row.instructions)
        category = str(row.category)

    recipe = Recipe(name, ingredients, instructions, category)
    return recipe
