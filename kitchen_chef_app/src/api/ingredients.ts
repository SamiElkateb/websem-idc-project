import axios, { AxiosResponse } from 'axios';
import serverConf from '../conf/server.conf';
import { TAutocompleteIngredient } from '../models/ingredients';

const getIngredients = async (): Promise<AxiosResponse<TAutocompleteIngredient[]>> => (axios.get(`${serverConf.URL}/ingredients`));

export { getIngredients };
