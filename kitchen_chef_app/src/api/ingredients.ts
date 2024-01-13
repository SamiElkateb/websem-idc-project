import axios, { AxiosResponse } from 'axios';
import serverConf from '../conf/server.conf';
import { TIngredient } from '../models/ingredients';

const getIngredients = async (): Promise<AxiosResponse<TIngredient[]>> => (axios.get(`${serverConf.URL}/ingredients`));

export { getIngredients };
