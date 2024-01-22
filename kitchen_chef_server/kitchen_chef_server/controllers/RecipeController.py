from typing import Annotated

from fastapi import HTTPException, Query
from kitchen_chef_server.conf import MICROSERVICE_HOSTNAME
from kitchen_chef_server.models.NutritionalData import NutritionalData
from kitchen_chef_server.models.RecipeFilter import RecipeFilter
from kitchen_chef_server.utils.corese_query import corese_query
from rdflib import Namespace, URIRef

from kitchen_chef_server.app import app
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
            initBindings[f"ingredientFood{i}"] = f"<{q_ingredient}>"

    if q_filters:
        for i, q_filter in enumerate(q_filters):
            initBindings[f"recipeFilter{i}"] = f"<{q_filter}>"

    if q_search_title:
        initBindings["recipeTitle"] = q_search_title

    results = corese_query(query, initBindings=initBindings)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes = []
    for index, row in results:
        recipe = Recipe(row.get("recipe"), row.get("name"), ingredients=[], instructions=row.get("instructions"),
                        category=row.get("category"), thumbnail=row.get("thumbnail"))
        recipes.append(recipe)

    return recipes


@app.get("/recipe")
async def get_recipe(recipe_identifier: str):
    """
    Une fois en cache, la requête prend ~5 secondes à s'exécuter
    """
    query = f"""
    prefix :        <http://project-kitchenchef.fr/schema#>
    prefix recipes: <http://project-kitchenchef.fr/recipes/data#>
    prefix skos:    <http://www.w3.org/2004/02/skos/core#>
    prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
    prefix dbo:    <http://dbpedia.org/ontology/>

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
            OPTIONAL {{ 
                SELECT * WHERE{{
                ?recipe :name ?recipeLabelTmp.
                FILTER(LANG(?recipeLabelTmp) = "en")
                }}LIMIT 1
             }}
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
            BIND(IF(BOUND(?recipeLabelTmp),?recipeLabelTmp,"No Label Found") AS ?recipeLabel)
            
            BIND(IF(BOUND(?ingredientQuantityStandard),?ingredientQuantityStandard,
            IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityImperial,
            IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityMetric, ""))) AS ?ingredientQuantity)
            
            BIND(IF(BOUND(?labelUnitStandard),?labelUnitStandard,
            IF(BOUND(?labelUnitImperial),?labelUnitImperial,
            IF(BOUND(?labelUnitMetric),?labelUnitMetric, ""))) AS ?labelUnit)
            BIND(IF(?labelUnit!="",CONCAT(?labelUnit," of "),?labelUnit) AS ?unit)
            
            BIND(STRBEFORE(STR(IF(BOUND(?labelUnitStandard) && ?labelUnitStandard = "Cup",8,1)*ROUND(?ingredientQuantity)),".") AS ?quantityQuery)
            BIND(LCASE(CONCAT(?quantityQuery," ",
            IF(?unit = "Cup of ","fluid ounces of ",?unit),?ingredientName)) AS ?query)

            BIND(IF(BOUND(?ingredientQuantityStandard),?ingredientQuantityStandard,"") AS ?ingredientQuantityStandardName)
            BIND(IF(BOUND(?ingredientQuantityImperial),?ingredientQuantityImperial,?ingredientQuantityStandardName) AS ?ingredientQuantityImperialName)
            BIND(IF(BOUND(?ingredientQuantityMetric),?ingredientQuantityMetric,?ingredientQuantityStandardName) AS ?ingredientQuantityMetricName)

            BIND(IF(BOUND(?labelUnitStandard),CONCAT(?labelUnitStandard," of "),"") AS ?labelUnitStandardName)
            BIND(IF(BOUND(?labelUnitImperial),CONCAT(?labelUnitImperial, " of "),?labelUnitStandardName) AS ?labelUnitImperialName)
            BIND(IF(BOUND(?labelUnitMetric),CONCAT(?labelUnitMetric," of "),?labelUnitStandardName) AS ?labelUnitMetricName)
        }} GROUP BY ?recipe
    }}
    BIND(CONCAT("http://{MICROSERVICE_HOSTNAME}/service/calorieninjas/nutrition?food=", ?queryList) AS ?urlMicroServ)

    {{
        SELECT * WHERE {{
            SERVICE ?urlMicroServ {{
                ?x :hasCalories ?kcal; :hasTotalFat ?fat; :hasCarbohydratesTotal ?carbs; :hasSugar ?sugar; :hasFiber ?fiber; :hasProtein ?proteins .
            }}
        }}
    }}
    }}
    """
    results = corese_query(
        query,
        initBindings={
            "uri": f"<{recipe_identifier}>",
        },
    )
    row_quantities = get_row(results)
    print("row_url", row_quantities)
    if debug:
        print("Label", row_quantities.get("recipeLabel"))
        print("URL", row_quantities.get("urlMicroServ"))
        print("Metrics : \n", row_quantities.get("ingredientMetricQuantities"), "\n",
              row_quantities.get("ingredientImperialQuantities"))
        print("Units : \n", row_quantities.get("labelUnitMetricNames"), "\n",
              row_quantities.get("labelUnitImperialNames"))
        print("Names : \n", row_quantities.get("ingredientNames"))
        print("X : \n", row_quantities.get("x"))

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
            FILTER(?recipe = <{recipe_identifier}>)
        }}GROUP BY ?recipe
    }}
    {{
        SELECT ?comment WHERE {{
            OPTIONAL {{
                SERVICE <https://dbpedia.org/sparql> {{
                    ?nameRecipe ^rdfs:label/dbo:abstract ?abstract .
                    FILTER(?nameRecipe = "{row_quantities.get("recipeLabel")}"@en && LANG(?abstract)="en")
                }}
            }}
            BIND(IF(BOUND(?abstract), ?abstract, "") AS ?comment)
        }}
    }}
    }}
    """
    results = corese_query(query)
    row_recipe = get_row(results)
    if debug:
        print("Kcal", row_quantities.get("kcal"), "Fat", row_quantities.get("fat"), "Carbs",
              row_quantities.get("carbs"), "Sugar", row_quantities.get("sugar"), "Fiber", row_quantities.get("fiber"),
              "Proteins", row_quantities.get("proteins"))
        try:
            print("Abstract", row_quantities.get("comment"))
        except Exception:
            print("No abstract found")
    ingredients = IngredientFactory.from_strings(
        row_recipe.get("ingredientIds"),
        row_quantities.get("ingredientNames"),
        row_recipe.get("ingredientFoods"),
        row_quantities.get("ingredientImperialQuantities"),
        row_quantities.get("labelUnitImperialNames"),
        row_quantities.get("ingredientMetricQuantities"),
        row_quantities.get("labelUnitMetricNames"),
    )
    nutritional_data = NutritionalData(row_quantities.get("kcal"), row_quantities.get("proteins"),
                                       row_quantities.get("fat"), row_quantities.get("carbs"),
                                       row_quantities.get("sugar"), row_quantities.get("fiber"))
    return Recipe(row_recipe.get("recipe"), row_recipe.get("name"), ingredients, row_recipe.get("instructions"),
                  row_recipe.get("category"), row_recipe.get("thumbnail"), row_recipe.get("comment"),
                  nutritional_data=nutritional_data)


def get_row(results):
    results = list(results)
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return results[0][1]


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

    results = corese_query(query)

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    recipes_filters = {}
    for index, row in results:
        recipe_filters = RecipeFilter(row.get("userRecipeFilter"), row.get("enUILabel"), row.get("frUILabel"))
        recipes_filters[row.get("userRecipeFilter")] = recipe_filters
    return list(recipes_filters.values())
