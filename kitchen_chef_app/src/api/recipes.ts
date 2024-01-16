import axios, { AxiosResponse } from 'axios';
import serverConf from '../conf/server.conf';
import { TRecipe } from '../models/recipes';
import { TIngredient } from '../models/ingredients';
import recipe from '../mock-data/recipe';

const getRecipes = async ({ filteringIngredients }: { filteringIngredients:TIngredient[] }): Promise<AxiosResponse<TRecipe[]>> => {
  const url = new URL(`${serverConf.URL}/recipes`);
  // filteringIngredients.forEach((ingredient) => url.searchParams.append('q_ingredients', ((new URL(ingredient.id)).hash.substr(1)).toString()));
  filteringIngredients.forEach((ingredient) => url.searchParams.append('q_ingredients', ingredient.id));
  return axios.get(url.toString());
};

const getRecipe = async (id: string) => axios.get(`${serverConf.URL}/recipe?recipe_identifier=${encodeURIComponent(id)}`);

export { getRecipe, getRecipes };
