import { TIngredient } from './ingredients';

export type TRecipe = {
  id :string
  name :string
  instructions :string
  category :string
  ingredients : TIngredient[]
  thumbnail: string
};
