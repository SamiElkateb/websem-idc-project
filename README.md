# Projet Kitchen Chef

## Objectif

### Uses cases
- Exprimer les recettes de cuisine dans différents systèmes de mesure (impérial, normal)
- Proposer les recettes possibles en fonction des ingrédients disponibles
- Trouver les ingrédients alternatifs (lait → lait d'avoine) ou la façon de remplacer un ingrédient avec plusieurs recettes
- Créer des instructions structurées à partir des consignes textuelles
- Scanner les codes barres pour récupérer les informations nutritionnelles d'un ingrédient
###  Recettes

Informations sur la recette (récupérée avec NLP sur Wikipédia etc)

#### CSV
Informations sur les ingrédients :
- type (legume, fruit, viande, etc)
- unités
- ingrédients

#### API

#### DBpedia

#### Inférence

- unitées de mesure (conversion)
- recette végétarienne / vegan / allergies

## TODO List

[x] Extraire le nom des ingrédients, convertir les unités \
[x] corriger l'erreur de blank node inutiles de csv to rdf \
[x] corriger les erreurs de food (cold, fry, etc) éventuellement Keyword Extraction ou un LLM \
[x] Recuperer recettes & ingredients\
[ ] Ajouter some pour toute les quantitées invalides ?\
[ ] Desambiguation des ingrédients et des recettes : extraction depuis textes\
[ ] SKOS : thesaurus aliments \
[ ] SKOS : thesaurus units (add top concepts) \
[ ] SKOS : thesaurus nutriments \
[ ] SHACL : à étoffer \
[ ] OWL : faire les inferences sur les recettes végétariennes / vegan \
[ ] OWL : étoffer vocabulaire\
[ ] OWL : recette allergies \
[x] µServices nutriments : ajouter une façon de trouver les calories et informations nutritionnelles à partir des recettes et ingrédients\
[ ] µServices : Query fédérée (utiliser endpoint web de données) \
[ ] OWL : Recettes transitives (ajouter des transformations d'ingrédients à partir de recettes)\
[ ] OWL : Aligner vocabulaires\
[ ] Server : faire le front\
[ ] Server : faire l'API\
[ ] Rapport\
[ ] Présentation

## Optionel 

[ ] utiliser https://fr.openfoodfacts.org pour avoir des informations plus juste sur les ingrédients à partir du code bar scanné sur application mobile\
[ ] Algo ML
## Pour les thesaurus

## CSV
https://github.com/cweber/cookbook/blob/master/recipes.csv
## APIS

https://calorieninjas.com/register

https://fr.openfoodfacts.org/data

https://fr.openfoodfacts.org
https://www.edamam.com/foods/?/apple
https://www.themealdb.com/api.php

## APP

Mobile:
- expo scan barcode:
Proposition de recette
calories adaptées aux produits scannés

## Web:
- Recherche par nom des recettes
- Filtres régime alimentaire, allergies (checkbox)
- Type de plats
- Listes des ingrédients souhaités
- Sort par nombre d'ingrédients manquants, ingrédients transformés, kcal

owl:
voc + transitivité des recttes
skos : Unites de mesures \
    aliments ?
SHACL : contraintes au pif, en fonction des besoins de l'appli

OWL + SKOS : 50% de la note
Préciser les langues, et s'assurer des types

sameAS : hasDBpediaEntity

csvw : https://github.com/cweber/cookbook/blob/master/recipes.csv
µService : API nutriments

Extraction avec dbpédia

Alignement avec dbpédia pour etre aligné sur les ingrédients
Unités aligné apres le csvw

### Quantitées

Few, Some, Many -> Unités pour un peu
Sinon entiers

Contraintes

Si a skos:Concept, pas le droit de a owl:Class. a skos:Concept, :Quantity c'est bon

## Tests
### Requêtes serveur

Récupérer les recettes filtrées par ingrédients:
http://localhost:8000/recipes?q_ingredients=Cornstarch&q_ingredients=Marshmallows
http://localhost:8000/recipes?q_ingredients=Cornstarch

Récupérer une recette:
http://localhost:8000/recipe?recipe_identifier=AngelHash

Récupérer tous les ingrédients:
http://localhost:8000/ingredients
