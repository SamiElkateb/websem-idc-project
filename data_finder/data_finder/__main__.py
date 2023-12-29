from utils.corese import Transformer
from utils.corese import export_to_file, load

recipes = load("../output/recipes.ttl")

export_to_file(recipes, Transformer.TURTLE, "../vocab/recipes.ttl")
