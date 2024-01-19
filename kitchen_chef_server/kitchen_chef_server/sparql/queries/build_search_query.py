def build_search_query(q_ingredients, q_filters):
    ingredients_query = ""
    if q_ingredients:
        for i, _ in enumerate(q_ingredients):
            ingredients_query += f"?recipe :hasIngredient ?ingredient{i} . ?ingredient{i} :food ?ingredientFood{i} ."
    query = f"""
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT DISTINCT ?recipe ?name ?category ?instructions ?thumbnail
            (group_concat(?ingredient; separator="|-|") AS ?ingredientIds)
            (group_concat(?ingredientFood; separator="|-|") AS ?ingredientFoods)
            (group_concat(?ingredientName; separator="|-|") AS ?ingredientNames)
            (group_concat(?ingredientQuantity; separator="|-|") AS ?ingredientQuantities)
            (group_concat(?ingredientUnit; separator="|-|") AS ?ingredientUnits)
    WHERE {{
        ?recipe a :Recipe ;
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
    }} GROUP BY ?recipe
    """
    return query
