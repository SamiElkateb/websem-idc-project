export type TIngredient = {
  name: string;
  id: string;
  thumbnail: string;
  imperialMeasure: {
    quantity: string;
    unit: string;
  },
  metricMeasure: {
    quantity: string;
    unit: string;
  }
};

export type TAutocompleteIngredient = {
  frLabel: string
  enLabel: string
  id: string
  thumbnail: string
};
