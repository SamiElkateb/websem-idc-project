import axios, { AxiosResponse } from 'axios';
import serverConf from '../conf/server.conf';
import { TRecipe } from '../models/recipes';

const getRecipes = async (): Promise<AxiosResponse<TRecipe[]>> => axios.get(`${serverConf.URL}/recipes`);

const getRecipe = async ({ id }: { id:string }) => axios.get(`${serverConf.URL}/recipe#${id}`);

export { getRecipe, getRecipes };
