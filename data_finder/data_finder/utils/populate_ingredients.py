from keybert import KeyBERT
from pke.unsupervised import MultipartiteRank
from rdflib import OWL, RDF, RDFS, DCTERMS, Graph, Literal, Namespace, URIRef
from utils.get_annotations import get_food_item

kw_model = KeyBERT()

FOOD = Namespace("http://project-kitchenchef.fr/food/data#")
SCHEMA = Namespace("http://project-kitchenchef.fr/schema#")


def to_pascal_case(text: str):
    return "".join(word.capitalize() for word in text.split())


added_food = {}


def add_food_item(g, ingredient_name, food_id, dbpedia_uri):
    q = """
        prefix : <http://project-kitchenchef.fr/schema#>
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix dbo:  <http://dbpedia.org/ontology/>
        INSERT {
            ?ingredient :food ?foodURI .
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

    if dbpedia_uri in added_food:
        return
    print("dbpedia_uri", dbpedia_uri)

    qres = g.query(
        """
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix dbo:  <http://dbpedia.org/ontology/>
        SELECT ?thumbnail ?label ?dcSubject
        WHERE {
          SERVICE <https://dbpedia.org/sparql> {
                ?dbpediaURI rdfs:label ?label ;
                            dbo:thumbnail ?thumbnail ;
                            dcterms:subject ?dcSubject .
          }
          FILTER (LANG(?label) = "fr" || LANG(?label) = "en")
        }
        """,
        initBindings={
            "dbpediaURI": URIRef(dbpedia_uri),
        },
    )
    food = {"dcterms:subject": []}

    for row in qres:
        food["thumbnail"] = row.thumbnail
        food[row.label.language] = row.label
        food["dcterms:subject"].append(row.dcSubject)
    frLabel = food.get("fr", None)
    if frLabel:
        g.add((FOOD[food_id], RDFS.label, Literal(frLabel, lang="fr")))

    enLabel = food.get("en", None)
    if enLabel:
        g.add((FOOD[food_id], RDFS.label, Literal(enLabel, lang="en")))
    thumbnail = food.get("thumbnail", None)
    if thumbnail:
        g.add((FOOD[food_id], SCHEMA["hasThumbnail"], URIRef(thumbnail)))

    for dcSubject in food["dcterms:subject"]:
        g.add((FOOD[food_id], DCTERMS.subject, URIRef(dcSubject)))

    g.add((FOOD[food_id], OWL.sameAs, URIRef(dbpedia_uri)))
    g.add((FOOD[food_id], RDF.type, SCHEMA["Food"]))

    added_food[dbpedia_uri] = True


query = """
        prefix :<http://project-kitchenchef.fr/schema#>

        SELECT DISTINCT ?ingredient ?ingredientName
        WHERE {
            ?ingredient a :Ingredient ;
            :name ?ingredientName
        }
        """


def populate_ingredients(g):
    qres = g.query(query)

    for row in qres:
        # print(row.ingredientName)
        ingredientName = str(row.ingredientName)

        keywords = kw_model.extract_keywords(
            ingredientName, keyphrase_ngram_range=(1, 3), stop_words=None
        )

        result = get_food_item(keywords)
        if not result:
            print(f"{row.ingredientName} not found")
            continue
        # if len(result) > 1:
        #     print(result)
        surfaceForm = to_pascal_case(result["surfaceForm"])
        dbpedia_uri = result["URI"]
        add_food_item(g, row.ingredientName, surfaceForm, dbpedia_uri)
    g.serialize(destination="../vocab/recipes.ttl")
