from urllib.parse import urlparse

from keybert import KeyBERT
from pke.unsupervised import MultipartiteRank
from rdflib import (DCTERMS, OWL, RDF, RDFS, SKOS, Graph, Literal, Namespace,
                    URIRef)
from utils.get_annotations import get_food_item
from utils.use_cache import load_cache, save_cache
from queries.food_thesaurus import food_thesaurus_query


def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)


kw_model = KeyBERT()

FOOD = Namespace("http://project-kitchenchef.fr/food/data#")
SCHEMA = Namespace("http://project-kitchenchef.fr/schema#")
DBP = Namespace("http://dbpedia.org/property/")


def to_pascal_case(text: str):
    return "".join(word.capitalize() for word in text.split())


added_food = {}
foods = load_cache("foods_cache")


def add_food_to_graph(g, food_id, dbpedia_uri, food):
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
        if dcSubject is None or not is_valid_url(dcSubject):
            continue
        g.add((FOOD[food_id], DCTERMS.subject, URIRef(dcSubject)))

    g.add((FOOD[food_id], OWL.sameAs, URIRef(dbpedia_uri)))
    g.add((FOOD[food_id], RDF.type, SCHEMA["Food"]))

    # Maybe:
    for dbpType in food["dbp:type"]:
        if dbpType is None or not is_valid_url(dbpType):
            continue
        g.add((FOOD[food_id], SKOS.broader, URIRef(dbpType)))

    g.add((FOOD[food_id], RDF.type, SKOS.Concept))

    pass


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
    if dbpedia_uri in foods.keys():
        add_food_to_graph(
            g=g, food_id=food_id, food=foods[dbpedia_uri], dbpedia_uri=dbpedia_uri
        )
        added_food[dbpedia_uri] = True
        return

    print("dbpedia_uri", dbpedia_uri)

    qres = g.query(
        """
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix dbo:  <http://dbpedia.org/ontology/>
        prefix dbp:  <http://dbpedia.org/property/>
        SELECT ?thumbnail ?label ?dcSubject ?dbpType
        WHERE {
          SERVICE <https://dbpedia.org/sparql> {
                ?dbpediaURI rdfs:label ?label .
                OPTIONAL {
                    ?dbpediaURI dbo:thumbnail ?thumbnail .
                }
                OPTIONAL {
                    ?dbpediaURI dcterms:subject ?dcSubject .
                }
                OPTIONAL {
                    ?dbpediaURI dbp:type ?dbpType .
                }
          }
          FILTER (LANG(?label) = "fr" || LANG(?label) = "en")
        }
        """,
        initBindings={
            "dbpediaURI": URIRef(dbpedia_uri),
        },
    )
    food = {"dcterms:subject": [], "dbp:type": []}

    for row in qres:
        food["thumbnail"] = row.thumbnail
        food[row.label.language] = row.label
        food["dcterms:subject"].append(row.dcSubject)
        food["dbp:type"].append(row.dbpType)
    add_food_to_graph(g=g, food_id=food_id, food=food, dbpedia_uri=dbpedia_uri)

    foods[dbpedia_uri] = food
    save_cache("foods_cache", foods)
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
    qres = g.update(food_thesaurus_query)
    g.serialize(destination="../vocab/recipes.ttl")
