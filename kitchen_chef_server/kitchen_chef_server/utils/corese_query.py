import json

import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper

from kitchen_chef_server.conf import CORESE_URL


def corese_query(query, initBindings={}):
    bound_query = query
    for key, value in initBindings.items():
        bound_query = bound_query.replace(f"?{key}", value)

    sparql = SPARQLWrapper(CORESE_URL)
    sparql.setQuery(bound_query)
    sparql.setReturnFormat(JSON)
    result = sparql.query()

    processed_results = json.load(result.response)
    print("PROCESSED_RESULTS", processed_results)
    cols = processed_results["head"]["vars"]

    out = []
    for row in processed_results["results"]["bindings"]:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get("value"))
        out.append(item)
    return (pd.DataFrame(out, columns=cols)).iterrows()
