FOOD_PREFIX = "prefix food:<http://project-kitchenchef.fr/food/data#>"
SCHEMA_PREFIX = ""


def food_prefix(value):
    return f"<http://project-kitchenchef.fr/food/data#{value}>"



def schema_prefix(value):
    return f"<http://project-kitchenchef.fr/schema#{value}>"
