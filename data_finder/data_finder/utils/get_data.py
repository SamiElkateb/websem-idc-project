import json
import os

from SPARQLWrapper import JSON, SPARQLWrapper


def get_data(uri: str, property="rdfs:comment", lang="en"):
    filename = uri.replace("http://dbpedia.org/resource/", "") + ".json"
    os.makedirs("datasets/twitter/cache", exist_ok=True)
    path = f"datasets/twitter/cache/{filename}"
    if os.path.isfile(path):
        with open(path, "r") as f:
            return json.load(f)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(
        f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?val
        WHERE {{
            <{uri}> {property} ?val .
            FILTER(langMatches(lang(?val), "{lang.upper()}"))
        }}"""
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = []

    for result in results["results"]["bindings"]:
        data.append(result["val"]["value"])
    if len(data) == 0:
        data = [""]
    with open(path, "w") as f:
        json.dump(data, f)
    return data
