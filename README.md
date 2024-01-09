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
- unitées de mesure
- recette végétarienne ou non
- allergies
## Déja fait
- Récupérer les recettes avec les ingrédients et les étapes de préparation
## À faire
[ ] Extraire le nom des ingrédients, convertir les unités
[x] corriger l'erreur de blank node inutiles de csv to rdf
[ ] corriger les erreurs de food (cold, fry, etc) éventuellement Keyword Extraction ou un LLM
[ ] ajouter des transformations d'ingrédients à partir de recettes (example: pates bolo)
[ ] ajouter une façon de trouver les calories et informations nutritionnelles à partir des recettes et ingrédients
[ ] utiliser https://fr.openfoodfacts.org pour avoir des informations plus juste sur les ingrédients à partir du code bar scanné sur application mobile


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

## Instructions

make all
run python  
