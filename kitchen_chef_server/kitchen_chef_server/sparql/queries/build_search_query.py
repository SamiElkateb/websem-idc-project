def build_search_query(q_ingredients, q_filters, q_search_title):
    ingredients_query = ""
    recipe_filter_query = ""
    recipe_search_title = ""
    if q_ingredients:
        for i, _ in enumerate(q_ingredients):
            ingredients_query += f"?recipe :hasIngredient ?ingredient{i} . ?ingredient{i} :food ?ingredientFood{i} ."
    if q_filters:
        for i, _ in enumerate(q_filters):
            recipe_filter_query += f"?recipeFilter{i}, "
    if q_search_title and q_search_title != "":
        recipe_search_title = f'FILTER(STRSTARTS(LCASE(STR(?name)), "{q_search_title.lower()}"))'

    query = f"""
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT DISTINCT ?recipe ?name ?category ?instructions ?thumbnail
            (group_concat(?ingredient; separator="|-|") AS ?ingredientIds)
            (group_concat(?ingredientFood; separator="|-|") AS ?ingredientFoods)
            (group_concat(?ingredientName; separator="|-|") AS ?ingredientNames)
            (group_concat(?ingredientQuantity; separator="|-|") AS ?ingredientQuantities)
            (group_concat(?ingredientUnit; separator="|-|") AS ?ingredientUnits)
    WHERE {{
        ?recipe a {recipe_filter_query} :Recipe ;
                :name ?name ;
                :hasIngredient ?ingredient ;
                :instructions ?instructions .

        OPTIONAL {{ ?recipe :hasThumbnail ?thumbnail . }}
        OPTIONAL {{ ?recipe :recipeCategory ?category . }}
        OPTIONAL {{ ?recipe :instructions ?instructions . }}

        ?ingredient :name ?ingredientName .
        OPTIONAL {{ ?ingredient :food ?ingredientFood . }}
        OPTIONAL {{ ?ingredient :quantity ?ingredientQuantity . }}
        OPTIONAL {{ ?ingredient :unit ?ingredientUnit . }}

        {ingredients_query}
        FILTER(!STRSTARTS(STR(?recipe), "http://dbpedia.org/resource"))
        {recipe_search_title}
    }}
    GROUP BY ?recipe
    ORDER BY desc(?thumbnail)
    """
    return query
