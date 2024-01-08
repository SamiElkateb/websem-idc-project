# Projet 

## Objectif

###  Recettes

Informations sur la recette (récupérée avec NLP sur wikipedia etc)

Informations sur les ingredients:
- type (legume, fruit, viande, etc)

Inférence:
- recette végétarienne ou non
- allergies


## À faire

- corriger l'erreur de blank node inutiles de csv to rdf
- corriger les erreurs de food (cold, fry, etc) éventuellement Keyword Extraction ou un LLM
- ajouter des transformations d'ingrédients à partir de recettes (example: pates bolo)

- ajouter une façon de trouver les calories et informations nutritionnelles à partir des recettes et ingrédients


- utiliser https://fr.openfoodfacts.org pour avoir des informations plus juste sur les ingrédients à partir du code bar scanné sur application mobile


## CSV

recipes.csv

table_ciqual.csv

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

Web:
- 
