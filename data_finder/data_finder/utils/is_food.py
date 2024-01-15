from rdflib import Graph, URIRef

from utils.use_cache import load_cache, save_cache

cache = load_cache("is_food_cache")


def check_is_food(dbpedia_uri):
    if cache.get(dbpedia_uri) is not None:
        return cache.get(dbpedia_uri)
    g = Graph()
    qres = g.query(
        """
        prefix owl:  <http://www.w3.org/2002/07/owl#>
        prefix dbo:  <http://dbpedia.org/ontology/>
        prefix dbp: <http://dbpedia.org/property/>
        SELECT ?dbpediaURI ?protein
        WHERE {
          SERVICE <https://dbpedia.org/sparql> {
              { ?dbpediaURI a dbo:Food }
              UNION
              { ?dbpediaURI dbp:protein ?protein }
              UNION
              { ?dbpediaURI dbo:protein ?protein }
              UNION
              { ?x dbo:ingredient ?dbpediaURI }
              UNION
              { ?y dbo:mainIngredient ?dbpediaURI }
              UNION
              { ?x dbp:ingredient ?dbpediaURI }
              UNION
              { ?y dbp:mainIngredient ?dbpediaURI }
          }
        }
        """,
        initBindings={
            "dbpediaURI": URIRef(dbpedia_uri),
        },
    )
    for _ in qres:
        cache[dbpedia_uri] = True
        save_cache("is_food_cache", cache)
        return True
    cache[dbpedia_uri] = False
    save_cache("is_food_cache", cache)
    return False
