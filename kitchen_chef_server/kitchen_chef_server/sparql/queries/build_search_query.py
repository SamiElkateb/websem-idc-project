def build_search_query(q_ingredients, q_filters):
    ingredients_query = ""
    for i, _ in enumerate(q_ingredients):
        ingredients_query += f"?recipe :hasIngredient ?ingredient{i} . ?ingredient{i} :food ?ingredientFood{i} ."
    query = f"""
    prefix :<http://project-kitchenchef.fr/schema#>
    SELECT DISTINCT ?recipe ?name ?category ?ingredientFood ?ingredient ?ingredientName ?ingredientQuantity ?instructions ?ingredientUnit WHERE {{
        ?recipe :name ?name ;
                :hasIngredient ?ingredient ;
                :instructions ?instructions ;
                :recipeCategory ?category .
        ?ingredient :food ?ingredientFood ;
                    :name ?ingredientName ;
                    :quantity ?ingredientQuantity ;
                    :unit ?ingredientUnit .

        {ingredients_query}
    }}
    """
    return query
