from kitchen_chef_server.models.Ingredient import Ingredient


class Recipe:
    def __init__(self, id, name, instructions, category):
        self.id = id
        self.name = name
        self.instructions = instructions
        self.category = category
        self.ingredients = []

    def add_ingredient(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)
