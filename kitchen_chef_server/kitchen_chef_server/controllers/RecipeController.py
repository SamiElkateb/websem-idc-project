from typing import Annotated

from fastapi import HTTPException, Query
from kitchen_chef_server.models.NutritionalData import NutritionalData
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


"""
Une fois en cache, la requête prend ~3 secondes à s'exécuter
"""
@app.get("/recipe")
async def get_recipe(recipe_identifier: str):
    query = """
    prefix :        <http://project-kitchenchef.fr/schema#>
    prefix recipes: <http://project-kitchenchef.fr/recipes/data#>
    prefix skos:    <http://www.w3.org/2004/02/skos/core#>
    
    SELECT * WHERE{
    {
        SELECT (group_concat(?query; separator=" and ") AS ?queryList)
        (group_concat(str(?ingredientName); separator="|-|") AS ?ingredientNames)
        (group_concat(str(?ingredientQuantityImperialName); separator="|-|") AS ?ingredientImperialQuantities)
        (group_concat(str(?ingredientQuantityMetricName); separator="|-|") AS ?ingredientMetricQuantities)
        (group_concat(str(?labelUnitImperialName); separator="|-|") AS ?labelUnitImperialNames)
        (group_concat(str(?labelUnitMetricName); separator="|-|") AS ?labelUnitMetricNames)
        WHERE {
            ?recipe :hasIngredient ?ingredient.
            ?ingredient :name ?ingredientName ;
            OPTIONAL { ?ingredient :hasStandardMeasurementUnit/:quantity ?ingredientQuantityStandard . }
            OPTIONAL { ?ingredient :hasStandardMeasurementUnit/:unit ?ingredientUnitTmp.
            OPTIONAL { ?ingredientUnitTmp skos:prefLabel ?prefLabelStandard }
            BIND(IF(BOUND(?prefLabelStandard),?prefLabelStandard,?ingredientUnitTmp) AS ?labelUnitStandard)
            }
            OPTIONAL { ?ingredient :hasImperialMeasurementUnit/:quantity ?ingredientQuantityImperial . }
            OPTIONAL { ?ingredient :hasImperialMeasurementUnit/:unit ?ingredientUnitTmp.
            ?ingredientUnitTmp skos:prefLabel ?labelUnitImperial}
            OPTIONAL { ?ingredient :hasMetricMeasurementUnit/:quantity ?ingredientQuantityMetric . }
            OPTIONAL { ?ingredient :hasMetricMeasurementUnit/:unit ?ingredientUnitTmp2 .
            ?ingredientUnitTmp2 skos:prefLabel ?labelUnitMetric}
            FILTER(?recipe = ?uri)
            BIND(IF(BOUND(?ingredientQuantityStandard),?ingredientQuantityStandard,
            IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityImperial,
            IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityMetric, ""))) AS ?ingredientQuantity)
            BIND(IF(BOUND(?labelUnitStandard),?labelUnitStandard,
            IF(BOUND(?labelUnitImperial),?labelUnitImperial,
            IF(BOUND(?labelUnitMetric),?labelUnitMetric, ""))) AS ?labelUnit)
            BIND(IF(?labelUnit!="",CONCAT(?labelUnit," of "),?labelUnit) AS ?unit)
            BIND(LCASE(CONCAT(STR(?ingredientQuantity)," ",?unit,?ingredientName)) AS ?query)

            BIND(IF(BOUND(?ingredientQuantityStandard),?ingredientQuantityStandard,"") AS ?ingredientQuantityStandardName)
            BIND(IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityImperial,?ingredientQuantityStandardName) AS ?ingredientQuantityImperialName)
            BIND(IF(BOUND(?ingredientQuantityMetric),?ingredientQuantityMetric,?ingredientQuantityStandardName) AS ?ingredientQuantityMetricName)

            BIND(IF(BOUND(?labelUnitStandard),?labelUnitStandard,"") AS ?labelUnitStandardName)
            BIND(IF(BOUND(?labelUnitImperial),?labelUnitImperial,?labelUnitStandardName) AS ?labelUnitImperialName)
            BIND(IF(BOUND(?labelUnitMetric),?labelUnitMetric,?labelUnitStandardName) AS ?labelUnitMetricName)
        } GROUP BY ?recipe
    }
    BIND(CONCAT("http://localhost/service/dbpedia/food?food=",REPLACE(?queryList," ","%20")) AS ?urlDbpedia)
    BIND(CONCAT("http://localhost/service/calorieninjas/nutrition?food=",REPLACE(?queryList," ","%20")) AS ?urlMicroServ)
    }
    """
    results = g.query(
        query,
        initBindings={
            "uri": URIRef(recipe_identifier),
        },
    )
    row_url = get_row(results)
    # print("URL", row_url.urlMicroServ)
    # print("URL dbpedia", row_url.urlDbpedia)
    # print("Metrics : \n", row_url.ingredientMetricQuantities, "\n", row_url.ingredientImperialQuantities)
    # print("Units : \n", row_url.labelUnitMetricNames, "\n", row_url.labelUnitImperialNames)
    # print("Names : \n", row_url.ingredientNames)

    query = f"""
    prefix :        <http://project-kitchenchef.fr/schema#>
    prefix recipes: <http://project-kitchenchef.fr/recipes/data#>
    prefix skos:    <http://www.w3.org/2004/02/skos/core#>
    
    SELECT * WHERE {{
        {{
            SELECT ?recipe ?name ?category ?instructions ?thumbnail
                (group_concat(?ingredient; separator="|-|") AS ?ingredientIds)
                (group_concat(?ingredientFood; separator="|-|") AS ?ingredientFoods)
            WHERE {{
                ?recipe :name ?name ;
                :hasIngredient ?ingredient .
                OPTIONAL {{ ?recipe :recipeCategory ?category . }}
                OPTIONAL {{ ?recipe :instructions ?instructions . }}
                OPTIONAL {{ ?recipe :hasThumbnail ?thumbnail . }}
                ?ingredient :food ?ingredientFood ;
                :name ?ingredientName ;
                OPTIONAL {{ ?ingredient :food ?ingredientFood . }}
                FILTER(?recipe = ?uri)
            }}GROUP BY ?recipe
        }}
        {{
            SELECT * WHERE {{
               SERVICE <{row_url.urlMicroServ}> {{
                    ?x :hasCalories ?kcal; :hasTotalFat ?fat; :hasCarbohydratesTotal ?carbs; :hasSugar ?sugar; :hasFiber ?fiber
                 }}
            }} 
        }}
        # {{
        #     SELECT * WHERE {{
        #         SERVICE <{row_url.urlDbpedia}> {{
        #             ?x :hasCalories ?kcal; :hasTotalFat ?fat; :hasCarbohydratesTotal ?carbs; :hasSugar ?sugar; :hasFiber ?fiber
        #     }}
        # }}
    }}
    """
    results = g.query(
        query,
        initBindings={
            "uri": URIRef(recipe_identifier),
        },
    )
    row = get_row(results)
    # print("Kcal", row.kcal, "Fat", row.fat, "Carbs", row.carbs, "Sugar", row.sugar, "Fiber", row.fiber)
    ingredients = IngredientFactory.from_strings(
        row.ingredientIds,
        row_url.ingredientNames,
        row.ingredientFoods,
        row_url.ingredientImperialQuantities,
        row_url.labelUnitImperialNames,
        row_url.ingredientMetricQuantities,
        row_url.labelUnitMetricNames,
    )
    nutritional_data = NutritionalData(row.kcal, row.fat, row.carbs, row.sugar, row.fiber)
    return Recipe(row.recipe, row.name, ingredients, nutritional_data, row.instructions, row.category, row.thumbnail)


def get_row(results):
    results = list(results)
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    row = results[0]
    return row
