from typing import Annotated
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from rdflib import Graph, Namespace, URIRef

import kitchen_chef_server.controllers.RecipeController
from kitchen_chef_server.app import app
from kitchen_chef_server.models.Ingredient import Ingredient
from kitchen_chef_server.models.Recipe import Recipe
from kitchen_chef_server.utils.load_graph import load_graph

