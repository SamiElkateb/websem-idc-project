from kitchen_chef_server.models.Ingredient import Ingredient


class Recipe:
    def __init__(
        self,
        id,
        name,
        ingredients,
        instructions,
        category,
        thumbnail,
        abstract,
        nutritional_data=None,
    ):
        self.id = id
        self.name = name
        self.instructions = instructions
        self.nutritionalData = nutritional_data
        self.category = category
        self.ingredients = ingredients
        self.thumbnail = thumbnail
        self.abstract = abstract
