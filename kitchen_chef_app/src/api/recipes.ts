import axios, { AxiosResponse } from 'axios';
import serverConf from '../conf/server.conf';
import { TRecipe } from '../models/recipes';
import { TAutocompleteIngredient } from '../models/ingredients';
import { TFilter } from '../models/others';

type TGetRecipe = { filteringIngredients: TAutocompleteIngredient[], recipeFilters: TFilter[],
  recipeSearchTitle: string };
const getRecipes = async ({ filteringIngredients, recipeFilters, recipeSearchTitle }:
TGetRecipe): Promise<AxiosResponse<TRecipe[]>> => {
  const url = new URL(`${serverConf.URL}/recipes`);
  filteringIngredients.forEach((ingredient) => url.searchParams.append('q_ingredients', ingredient.id));
  recipeFilters.filter((item) => item.active).forEach((item) => url.searchParams.append('q_filters', item.id));
  if (recipeSearchTitle !== '') {
    url.searchParams.append('q_search_title', recipeSearchTitle);
  }
  return axios.get(url.toString());
};

const getRecipe = async (id: string) => axios.get(`${serverConf.URL}/recipe?recipe_identifier=${encodeURIComponent(id)}`);

const getRecipeFilters = async (): Promise<AxiosResponse<Omit<TFilter, 'active'>[]>> => (axios.get(`${serverConf.URL}/recipe_filters`));

export { getRecipe, getRecipes, getRecipeFilters };
