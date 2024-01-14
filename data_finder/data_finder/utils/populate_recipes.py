import wikipedia
from keybert import KeyBERT
from pke.unsupervised import MultipartiteRank
from rdflib import OWL, RDF, RDFS, Graph, Literal, Namespace, URIRef

kw_model = KeyBERT()

FOOD = Namespace("http://project-kitchenchef.fr/food/data#")
RECIPES = Namespace("http://project-kitchenchef.fr/recipes/data#")
SCHEMA = Namespace("http://project-kitchenchef.fr/schema#")


def to_pascal_case(text: str):
    return "".join(word.capitalize() for word in text.split())


def get_dbpedia_uri(g, wikipedia_uri):
    qres = g.query(
        """
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix dbo:  <http://dbpedia.org/ontology/>
        SELECT ?dbpediaURI
        WHERE {
          SERVICE <https://dbpedia.org/sparql> {
                ?dbpediaURI foaf:isPrimaryTopicOf ?wikipediaURI .
                ?dbpediaURI a dbo:Food .
          }
        }
        """,
        initBindings={
            "wikipediaURI": URIRef(wikipedia_uri),
        },
    )
    for row in qres:
        return row.dbpediaURI


def add_recipe_data(g, recipe_uri, dbpedia_uri):
    qres = g.query(
        """
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix dbo:  <http://dbpedia.org/ontology/>
        SELECT ?thumbnail ?label
        WHERE {
          SERVICE <https://dbpedia.org/sparql> {
                ?dbpediaURI rdfs:label ?label ;
                            dbo:thumbnail ?thumbnail .
          }
          FILTER (LANG(?label) = "fr" || LANG(?label) = "en")
        }
        """,
        initBindings={
            "dbpediaURI": URIRef(dbpedia_uri),
        },
    )
    recipe = {}

    for row in qres:
        recipe["thumbnail"] = row.thumbnail
        recipe[row.label.language] = row.label
    frLabel = recipe.get("fr", None)
    if frLabel:
        g.add((URIRef(recipe_uri), RDFS.label, Literal(frLabel, lang="fr")))

    enLabel = recipe.get("en", None)
    if enLabel:
        g.add((URIRef(recipe_uri), RDFS.label, Literal(enLabel, lang="en")))
    thumbnail = recipe.get("thumbnail", None)
    if thumbnail:
        g.add((URIRef(recipe_uri), SCHEMA["hasThumbnail"], URIRef(thumbnail)))
    g.add((URIRef(recipe_uri), OWL.sameAs, URIRef(dbpedia_uri)))


query = """
        prefix :<http://project-kitchenchef.fr/schema#>

        SELECT DISTINCT ?recipe ?recipeName
        WHERE {
            ?recipe a :Recipe ;
            :name ?recipeName
        }
        """


def populate_recipes(g):
    qres = g.query(query)

    for row in qres:
        try:
            recipeName = str(row.recipeName)
            results = wikipedia.search(recipeName, results=1)
            if not results:
                print(f"{row.recipeName} not found")
                continue
            page = wikipedia.page(results[0])
            wikipedia_URI = page.url.replace("https", "http")
            dbpedia_uri = get_dbpedia_uri(g, wikipedia_URI)
            if not dbpedia_uri:
                print(f"{row.recipeName} not found: ", dbpedia_uri, " not a food")
                continue
            print("RecipeName: ", row.recipeName,  "Page: ", dbpedia_uri)
            add_recipe_data(g, row.recipe, dbpedia_uri)
        except Exception as e:
            pass
    g.serialize(destination="../vocab/recipes.ttl")
