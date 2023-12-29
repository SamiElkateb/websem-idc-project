from rdflib import Graph, Namespace, URIRef
from utils.get_annotations import get_food_item

g = Graph()
g.parse("../output/recipes.ttl")

FOOD = Namespace("http://project-kitchenchef.fr/food/data#")


def to_pascal_case(text: str):
    return ''.join(word.capitalize() for word in text.split())


def add_food_item(ingredient_name, food_id, dbpedia_uri):
    q = """
        prefix : <http://project-kitchenchef.fr/schema#>
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix food: <http://project-kitchenchef.fr/food/data#>
        INSERT {
            ?ingredient :food ?foodURI .
            ?foodURI owl:sameAs ?dbpediaURI .
        } WHERE {
            ?ingredient a :Ingredient .
            ?ingredient :name ?ingredientName .
        }
        """
    g.update(
        q,
        initBindings={
            "ingredientName": ingredient_name,
            "foodURI": FOOD[food_id],
            "dbpediaURI": URIRef(dbpedia_uri),
        },
    )


query = """
        prefix :<http://project-kitchenchef.fr/schema#>

        SELECT DISTINCT ?ingredient ?ingredientName
        WHERE {
            ?ingredient a :Ingredient ;
            :name ?ingredientName
        }
        """


qres = g.query(query)

for row in qres:
    result = get_food_item(row.ingredientName)
    if not result:
        print(f"{row.ingredientName} not found")
        continue
    surfaceForm = to_pascal_case(result[0]["surfaceForm"])
    dbpedia_uri = result[0]["URI"]
    add_food_item(row.ingredientName, surfaceForm, dbpedia_uri)


g.serialize(destination="../vocab/recipes.ttl")
