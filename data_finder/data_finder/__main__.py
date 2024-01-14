from rdflib import Graph
from utils.populate_ingredients import populate_ingredients
from utils.populate_recipes import populate_recipes

g = Graph()
g.parse("../vocab/recipes.ttl")

populate_ingredients(g)
# populate_recipes(g)
