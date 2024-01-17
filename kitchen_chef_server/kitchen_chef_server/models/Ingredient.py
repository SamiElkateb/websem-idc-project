class Ingredient:
    def __init__(self, id, foodIdentifier, name, imperialQuantity, imperialUnit, metricQuantity, metricUnit):
        self.id = id
        self.foodIdentifier = foodIdentifier
        self.name = name
        self.imperialMeasure = {"quantity": imperialQuantity, "unit": imperialUnit}
        self.metricMeasure = {"quantity": metricQuantity, "unit": metricUnit}
