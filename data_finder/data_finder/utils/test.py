import json
import os

import pandas as pd
import spotlight
from SPARQLWrapper import JSON, SPARQLWrapper

DB_SPOTLIGHT_URL = "https://api.dbpedia-spotlight.org/en/annotate"

TEXT = """
With an equilibrium temperature of about 4,050 kelvin, the exoplanet KELT-9b (also known as
HD 195689b) is an archetype of the class of ultrahot Jupiters that straddle the transition between
stars and gas-giant exoplanets and are therefore useful for studying atmospheric chemistry
"""

VAL = pd.read_csv("./datasets/twitter/VAL.csv")

SELECTED_DATA = pd.DataFrame({"a": ["Cherry"]})


def get_annotations(texts: list | str, confidence=0.6, support=20):
    if type(texts) == list:
        data = []
        for text in texts:
            annotations = spotlight.annotate(
                DB_SPOTLIGHT_URL, text, confidence=confidence, support=support
            )
            data.append(annotations)
        return data
    else:
        return spotlight.annotate(DB_SPOTLIGHT_URL, texts, confidence=0.1, support=10)


def print_annotations(annotations: list):
    for annotation in annotations:
        print(f"URI: {annotation['URI']}")
        print(f"support: {annotation['support']}")
        print(f"types: {annotation['types']}")
        print(f"surfaceForm: {annotation['surfaceForm']}")
        print(f"offset: {annotation['offset']}")
        print(f"similarityScore: {annotation['similarityScore']}")
        print(f"percentageOfSecondRank: {annotation['percentageOfSecondRank']}")
        print()


def extract_uris(annotations: list):
    uris = []
    for annotation in annotations:
        uris.append(annotation["URI"])
    return uris


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


for key, text in SELECTED_DATA.iterrows():
    tweet = str(text.iloc[0])
    annotations = get_annotations(tweet)
    final_text = tweet
    print("TWEET: ", tweet, end="\n\n")

    meta_offset = 0

    print("ENTITIES: ")
    for annotation in annotations:
        data = get_data(annotation["URI"])
        print(
            f'  <entity URI="{annotation["URI"]}>{annotation["surfaceForm"]}</entity>'
        )
        truncated_abstract = " [" + data[0][:50] + " ...]" if len(data[0]) > 49 else ""
        index = final_text.find(" ", annotation["offset"] + meta_offset)
        if index != -1:
            final_text = final_text[:index] + truncated_abstract + final_text[index:]
        else:
            final_text = final_text + truncated_abstract

        meta_offset += len(truncated_abstract)

    print("\n ENRICHED_TWEET: ", final_text, end="\n\n")
    print(
        "--------------------------------------------------------------------------------"
    )
    print(
        "--------------------------------------------------------------------------------"
    )
