food_thesaurus_query = """
prefix dbpediaCategory: <http://dbpedia.org/resource/Category:>
prefix dcterms: <http://purl.org/dc/terms/>
prefix food: <http://project-kitchenchef.fr/food/data#>

DELETE { ?x dcterms:subject ?z .}
INSERT {
  ?fruit skos:broaderTransitive food:Fruit .
  ?vegetable skos:broaderTransitive food:Vegetable .
  ?dairyProduct skos:broaderTransitive food:DairyProduct .
  ?cheese skos:broaderTransitive food:Cheese .
  ?animalProduct skos:broaderTransitive food:animalProduct .
  ?meat skos:broaderTransitive food:Meat .
  ?eggs skos:broaderTransitive food:Eggs .
  ?fish skos:broaderTransitive food:Fish .
  ?seaFood skos:broaderTransitive food:SeaFood .
  ?bread skos:broaderTransitive food:Bread .
  ?pasta skos:broaderTransitive food:Pasta .
  ?spice skos:broaderTransitive food:Spice .
  ?condiment skos:broaderTransitive food:Condiment .
  ?nuts skos:broaderTransitive food:Nuts .
  ?arachis skos:broaderTransitive food:Arachis .
  ?cereals skos:broaderTransitive food:Cereals .
} WHERE {
  { ?x dcterms:subject ?z . } UNION
  { ?fruit dcterms:subject dbpediaCategory:Edible_fruits . } UNION
  { ?fruit dcterms:subject dbpediaCategory:Dried_fruit . } UNION
  { ?fruit dcterms:subject dbpediaCategory:Berries . } UNION
  { ?fruit dcterms:subject dbpediaCategory:Fruit_trees . } UNION
  { ?fruit dcterms:subject dbpediaCategory:Fruit_juice . } UNION


  { ?vegetable dcterms:subject dbpediaCategory:Root_vegetables . } UNION
  { ?vegetable dcterms:subject dbpediaCategory:Vegetables . } UNION
  { ?vegetable dcterms:subject dbpediaCategory:Plant-based_fermented_foods . } UNION
  { ?vegetable dcterms:subject dbpediaCategory:Leaf_vegetables . }
  { ?vegetable dcterms:subject dbpediaCategory:Fruit_vegetables . } UNION
  { ?vegetable dcterms:subject dbpediaCategory:Edible_legumes . } UNION
  { ?vegetable dcterms:subject dbpediaCategory:Legumes . } UNION
  { ?vegetable dcterms:subject dbpediaCategory:Stem_vegetables . } UNION


  { ?cheese dcterms:subject dbpediaCategory:Processed_cheese . } UNION
  { ?cheese dcterms:subject dbpediaCategory:American_cheeses . } UNION
  { ?cheese dcterms:subject dbpediaCategory:Acid-set_cheeses . } UNION
  { ?cheese dcterms:subject dbpediaCategory:Cow%27s-milk_cheeses . } UNION
  { ?cheese dcterms:subject dbpediaCategory:Smoked_cheeses . } UNION
  { ?cheese dcterms:subject dbpediaCategory:Stretched-curd_cheeses . } UNION
  { ?cheese dcterms:subject dbpediaCategory:Cream_cheeses . } UNION

  { ?dairyProduct dcterms:subject dbpediaCategory:Dairy_products . } UNION
  { ?dairyProduct dcterms:subject dbpediaCategory:Milk-based_drinks . } UNION
  { ?dairyProduct dcterms:subject dbpediaCategory:Fermented_dairy_products . } UNION

  { ?animalProduct dcterms:subject dbpediaCategory:Animal_products . } UNION

  { ?meat dcterms:subject dbpediaCategory:Meat . } UNION
  { ?meat dcterms:subject dbpediaCategory:Poultry . } UNION
  { ?meat dcterms:subject dbpediaCategory:Beef . } UNION
  { ?meat dcterms:subject dbpediaCategory:Poultry_products . } UNION
  { ?meat dcterms:subject dbpediaCategory:Fried_chicken . } UNION
  { ?meat dcterms:subject dbpediaCategory:Ground_meat . } UNION
  { ?meat dcterms:subject dbpediaCategory:Charcuterie . } UNION
  { ?meat dcterms:subject dbpediaCategory:Smoked_meat . } UNION
  { ?meat dcterms:subject dbpediaCategory:Cuts_of_beef . } UNION
  { ?meat dcterms:subject dbpediaCategory:Cattle_products . } UNION
  { ?meat dcterms:subject dbpediaCategory:Meat_by_animal . } UNION
  { ?meat dcterms:subject dbpediaCategory:Bacon . } UNION

  { ?eggs dcterms:subject dbpediaCategory:Eggs . } UNION

  { ?fish dcterms:subject dbpediaCategory:Sport_fish . } UNION
  { ?fish dcterms:subject dbpediaCategory:Commercial_fish . } UNION
  { ?fish dcterms:subject dbpediaCategory:Fish_processing . } UNION
  { ?fish dcterms:subject dbpediaCategory:Fish . } UNION

  { ?seaFood dcterms:subject dbpediaCategory:Commercial_molluscs . } UNION
  { ?seaFood dcterms:subject dbpediaCategory:Edible_crustaceans . } UNION
  { ?seaFood dcterms:subject dbpediaCategory:Seafood . } UNION

  { ?bread dcterms:subject dbpediaCategory:Flatbreads . } UNION
  { ?bread dcterms:subject dbpediaCategory:Breads . } UNION

  { ?pasta dcterms:subject dbpediaCategory:Types_of_pasta . } UNION
  { ?pasta dcterms:subject dbpediaCategory:Pasta . } UNION

  { ?spice dcterms:subject dbpediaCategory:Herb_and_spice_mixtures . } UNION
  { ?spice dcterms:subject dbpediaCategory:Herbs . } UNION
  { ?spice dcterms:subject dbpediaCategory:Spices . } UNION
  { ?condiments dcterms:subject dbpediaCategory:Condiments . } UNION

  { ?nuts dcterms:subject dbpediaCategory:Edible_nuts_and_seeds . } UNION

  { ?arachis dcterms:subject dbpediaCategory:Arachis . } UNION
  { ?arachis dcterms:subject dbpediaCategory:Peanut_butter . } UNION
  { ?cereals dcterms:subject dbpediaCategory:Cereals . }
}

"""
