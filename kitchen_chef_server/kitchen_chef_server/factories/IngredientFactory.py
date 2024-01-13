from kitchen_chef_server.models.Ingredient import Ingredient


class IngredientFactory:
    @staticmethod
    def from_lists(
        ingredient_ids,
        ingredient_names,
        ingredient_foods,
        ingredient_quantities,
        ingredient_units,
    ):
        ingredients = []
        for id, name, food, quantity, unit in zip(
            ingredient_ids,
            ingredient_names,
            ingredient_foods,
            ingredient_quantities,
            ingredient_units,
        ):
            ingredients.append(Ingredient(id, food, name, quantity, unit))

        return ingredients

    @staticmethod
    def from_strings(
        ingredient_ids,
        ingredient_names,
        ingredient_foods,
        ingredient_quantities,
        ingredient_units,
    ):
        return IngredientFactory.from_lists(
            ingredient_ids.split("|-|"),
            ingredient_names.split("|-|"),
            ingredient_foods.split("|-|"),
            ingredient_quantities.split("|-|"),
            ingredient_units.split("|-|"),
        )
