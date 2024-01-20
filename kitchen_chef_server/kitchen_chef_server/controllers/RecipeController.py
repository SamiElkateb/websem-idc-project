from typing import Annotated

from fastapi import HTTPException, Query
from kitchen_chef_server.conf import MICROSERVICE_HOSTNAME
from kitchen_chef_server.models.NutritionalData import NutritionalData
from kitchen_chef_server.models.RecipeFilter import RecipeFilter
from rdflib import Namespace, URIRef

from kitchen_chef_server.app import app, g
from kitchen_chef_server.factories.IngredientFactory import IngredientFactory
from kitchen_chef_server.models.Ingredient import Ingredient
from kitchen_chef_server.models.Recipe import Recipe
from kitchen_chef_server.sparql.queries.build_search_query import \
    build_search_query


RECIPES = Namespace("http://project-kitchenchef.fr/recipes/data#")
FOODS = Namespace("http://project-kitchenchef.fr/food/data#")
debug = True


# TODO: query parameters: filter ingredients
@app.get("/recipes")
async def get_recipes(
        q_ingredients: Annotated[list[str] | None, Query()] = None,
        q_filters: Annotated[list[str] | None, Query()] = None,
        q_search_title: Annotated[str | None, Query()] = None,
):
    q_ingredients = q_ingredients if q_ingredients else []
    q_filters = q_filters if q_filters else []
    query = build_search_query(q_ingredients, q_filters, q_search_title)
    initBindings = {}
    if q_ingredients:
        for i, q_ingredient in enumerate(q_ingredients):
            initBindings[f"ingredientFood{i}"] = URIRef(q_ingredient)

    if q_filters:
        for i, q_filter in enumerate(q_filters):
            initBindings[f"recipeFilter{i}"] = URIRef(q_filter)

    if q_search_title:
        initBindings["recipeTitle"] = q_search_title

    results = g.query(query, initBindings=initBindings)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes = []
    for row in results:
        recipe = Recipe(row.recipe, row.name, ingredients=[], instructions=row.instructions, category=row.category, thumbnail=row.thumbnail)
        recipes.append(recipe)

    return recipes


@app.get("/recipe")
async def get_recipe(recipe_identifier: str):
    """
    Une fois en cache, la requête prend ~3 secondes à s'exécuter
    """
    query = f"""
    prefix :        <http://project-kitchenchef.fr/schema#>
    prefix recipes: <http://project-kitchenchef.fr/recipes/data#>
    prefix skos:    <http://www.w3.org/2004/02/skos/core#>
    prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#>

    SELECT * WHERE{{
    {{
        SELECT ?recipeLabel
        (group_concat(?query; separator=" and ") AS ?queryList)
        (group_concat(str(?ingredientName); separator="|-|") AS ?ingredientNames)
        (group_concat(str(?ingredientQuantityImperialName); separator="|-|") AS ?ingredientImperialQuantities)
        (group_concat(str(?ingredientQuantityMetricName); separator="|-|") AS ?ingredientMetricQuantities)
        (group_concat(str(?labelUnitImperialName); separator="|-|") AS ?labelUnitImperialNames)
        (group_concat(str(?labelUnitMetricName); separator="|-|") AS ?labelUnitMetricNames)
        WHERE {{
            ?recipe :hasIngredient ?ingredient.
            OPTIONAL {{ ?recipe rdfs:label ?recipeLabelTmp.
             FILTER(LANG(?recipeLabelTmp) = "en")}}
            ?ingredient :name ?ingredientName ;
            OPTIONAL {{ ?ingredient :hasStandardMeasurementUnit/:quantity ?ingredientQuantityStandard . }}
            OPTIONAL {{ ?ingredient :hasStandardMeasurementUnit/:unit ?ingredientUnitTmp.
                OPTIONAL {{ ?ingredientUnitTmp skos:prefLabel ?labelUnitStandard }}
            }}
            OPTIONAL {{ ?ingredient :hasImperialMeasurementUnit/:quantity ?ingredientQuantityImperial . }}
            OPTIONAL {{ ?ingredient :hasImperialMeasurementUnit/:unit ?ingredientUnitTmp.
            ?ingredientUnitTmp skos:prefLabel ?labelUnitImperial}}
            OPTIONAL {{ ?ingredient :hasMetricMeasurementUnit/:quantity ?ingredientQuantityMetric . }}
            OPTIONAL {{ ?ingredient :hasMetricMeasurementUnit/:unit ?ingredientUnitTmp2 .
            ?ingredientUnitTmp2 skos:prefLabel ?labelUnitMetric}}
            FILTER(?recipe = ?uri)
            BIND(IF(BOUND(?recipeLabelTmp),?recipeLabelTmp,"") AS ?recipeLabel)
            
            BIND(IF(BOUND(?ingredientQuantityStandard),?ingredientQuantityStandard,
            IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityImperial,
            IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityMetric, ""))) AS ?ingredientQuantity)
            
            BIND(IF(BOUND(?labelUnitStandard),?labelUnitStandard,
            IF(BOUND(?labelUnitImperial),?labelUnitImperial,
            IF(BOUND(?labelUnitMetric),?labelUnitMetric, ""))) AS ?labelUnit)
            BIND(IF(?labelUnit!="",CONCAT(?labelUnit," of "),?labelUnit) AS ?unit)
            
            BIND(LCASE(CONCAT(STR(IF(BOUND(?labelUnitStandard) && ?labelUnitStandard = "Cup",8,1)*ROUND(?ingredientQuantity))," ",
            IF(?unit = "Cup of ","fluid ounces of ",?unit),?ingredientName)) AS ?query)

            BIND(IF(BOUND(?ingredientQuantityStandard),?ingredientQuantityStandard,"") AS ?ingredientQuantityStandardName)
            BIND(IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityImperial,?ingredientQuantityStandardName) AS ?ingredientQuantityImperialName)
            BIND(IF(BOUND(?ingredientQuantityMetric),?ingredientQuantityMetric,?ingredientQuantityStandardName) AS ?ingredientQuantityMetricName)

            BIND(IF(BOUND(?labelUnitStandard),CONCAT(?labelUnitStandard," of "),"") AS ?labelUnitStandardName)
            BIND(IF(BOUND(?labelUnitImperial),CONCAT(?labelUnitImperial, " of "),?labelUnitStandardName) AS ?labelUnitImperialName)
            BIND(IF(BOUND(?labelUnitMetric),CONCAT(?labelUnitMetric," of "),?labelUnitStandardName) AS ?labelUnitMetricName)
        }} GROUP BY ?recipe
    }}
    BIND(CONCAT("http://{MICROSERVICE_HOSTNAME}/service/calorieninjas/nutrition?food=",ENCODE_FOR_URI(?queryList)) AS ?urlMicroServ)
    }}
    """
    results = g.query(
        query,
        initBindings={
            "uri": URIRef(recipe_identifier),
        },
    )
    row_url = get_row(results)
    if debug:
        print("Label",row_url.recipeLabel)
        print("URL", row_url.urlMicroServ)
        print("Metrics : \n", row_url.ingredientMetricQuantities, "\n", row_url.ingredientImperialQuantities)
        print("Units : \n", row_url.labelUnitMetricNames, "\n", row_url.labelUnitImperialNames)
        print("Names : \n", row_url.ingredientNames)

    query = f"""
    prefix :        <http://project-kitchenchef.fr/schema#>
    prefix recipes: <http://project-kitchenchef.fr/recipes/data#>
    prefix skos:    <http://www.w3.org/2004/02/skos/core#>
    prefix dbo:    <http://dbpedia.org/ontology/>
    prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT * WHERE {{
    {{
        SELECT ?recipe ?name ?category ?instructions ?thumbnail
        (group_concat(?ingredient; separator="|-|") AS ?ingredientIds)
        (group_concat(?ingredientFood; separator="|-|") AS ?ingredientFoods)
        WHERE {{
            ?recipe :hasIngredient ?ingredient ; :name ?name .
            OPTIONAL {{ ?recipe :recipeCategory ?category . }}
            OPTIONAL {{ ?recipe :instructions ?instructions . }}
            OPTIONAL {{ ?recipe :hasThumbnail ?thumbnail . }}
            ?ingredient :food ?ingredientFood ;
            :name ?ingredientName ;
            OPTIONAL {{ ?ingredient :food ?ingredientFood . }}
            FILTER(?recipe = <{URIRef(recipe_identifier)}>)
        }}GROUP BY ?recipe
    }}
    {{
        SELECT * WHERE {{
            SERVICE <{row_url.urlMicroServ}> {{
                ?x :hasCalories ?kcal; :hasTotalFat ?fat; :hasCarbohydratesTotal ?carbs; :hasSugar ?sugar; :hasFiber ?fiber; :hasProtein ?proteins .
            }}
        }}
    }}
    {{
        SELECT ?comment WHERE {{
            OPTIONAL {{
                SERVICE <https://dbpedia.org/sparql> {{
                    ?nameRecipe ^rdfs:label/dbo:abstract ?abstract .
                    FILTER(?nameRecipe = "{row_url.recipeLabel}"@en && LANG(?abstract)="en")
                }}
            }}
            BIND(IF(BOUND(?abstract), ?abstract, "") AS ?comment)
        }}
    }}
    }}
    """
    results = g.query(
        query
    )
    row = get_row(results)
    if debug:
        print("Kcal", row.kcal, "Fat", row.fat, "Carbs", row.carbs, "Sugar", row.sugar, "Fiber", row.fiber, "Proteins", row.proteins)
        try:
            print("Abstract", row.comment)
        except Exception:
            print("No abstract found")
    ingredients = IngredientFactory.from_strings(
        row.ingredientIds,
        row_url.ingredientNames,
        row.ingredientFoods,
        row_url.ingredientImperialQuantities,
        row_url.labelUnitImperialNames,
        row_url.ingredientMetricQuantities,
        row_url.labelUnitMetricNames,
    )
    nutritional_data = NutritionalData(row.kcal, row.proteins, row.fat, row.carbs, row.sugar, row.fiber)
    return Recipe(row.recipe, row.name, ingredients, row.instructions, row.category, row.thumbnail,row.comment, nutritional_data=nutritional_data)

def get_row(results):
    results = list(results)
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return results[0]

@app.get("/recipe_filters")
async def get_recipe_filters():
    query = """
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT DISTINCT ?userRecipeFilter ?frUILabel ?enUILabel WHERE {
           ?userRecipeFilter a :UserRecipeFilter ;
           :uiLabel ?frUILabel ;
           :uiLabel ?enUILabel .
           FILTER (LANG(?frUILabel) = "fr")
           FILTER (LANG(?enUILabel) = "en")
    }
    """

    results = g.query(
        query,
    )

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes_filters = {}
    for row in results:
        recipe_filters = RecipeFilter(row.userRecipeFilter, row.enUILabel, row.frUILabel)
        recipes_filters[row.userRecipeFilter] = recipe_filters
    return list(recipes_filters.values())
