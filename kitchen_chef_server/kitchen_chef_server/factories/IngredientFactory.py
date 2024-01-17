from kitchen_chef_server.models.Ingredient import Ingredient


class IngredientFactory:
    @staticmethod
    def from_lists(
        ingredient_ids,
        ingredient_names,
        ingredient_foods,
        imperial_quantities,
        imperial_units,
        metric_quantities,
        metric_units,
    ):
        ingredients = []
        for (
            id,
            name,
            food,
            imperial_quantity,
            imperial_unit,
            metric_quantity,
            metric_unit,
        ) in zip(
            ingredient_ids,
            ingredient_names,
            ingredient_foods,
            imperial_quantities,
            imperial_units,
            metric_quantities,
            metric_units,
        ):
            ingredients.append(
                Ingredient(
                    id,
                    food,
                    name,
                    imperial_quantity,
                    imperial_unit,
                    metric_quantity,
                    metric_unit,
                )
            )

        return ingredients

    @staticmethod
    def from_strings(
        ingredient_ids,
        ingredient_names,
        ingredient_foods,
        imperial_quantities,
        imperial_units,
        metric_quantities,
        metric_units,
    ):
        return IngredientFactory.from_lists(
            ingredient_ids.split("|-|"),
            ingredient_names.split("|-|"),
            ingredient_foods.split("|-|"),
            imperial_quantities.split("|-|"),
            imperial_units.split("|-|"),
            metric_quantities.split("|-|"),
            metric_units.split("|-|"),
        )
