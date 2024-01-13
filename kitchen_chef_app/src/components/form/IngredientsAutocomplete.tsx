import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { TIngredient } from '../../models/ingredients';

type IngredientsAutocompleteProps = {
  onAddIngredient: (item: TIngredient) => void
  availableIngredients: TIngredient[]
};

const IngredientsAutocomplete: React.FC<IngredientsAutocompleteProps> = ({
  onAddIngredient,
  availableIngredients,
}) => {
  const [ingredient, setIngredient] = useState<TIngredient>();

  const handleAddClick = () => {
    if (ingredient) {
      onAddIngredient(ingredient);
      setIngredient(undefined);
    }
  };

  return (
    <div>
      <Autocomplete
        onChange={(_, newValue) => {
          setIngredient(newValue);
        }}
        getOptionLabel={(option) => option.frLabel}
        options={availableIngredients}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Ingredient"
            onKeyDown={(e) => {
              if ((e.code === 'Enter' || e.code === 'enter') && e.target.value) {
                handleAddClick();
              }
            }}
          />
        )}
        size="small"
      />
    </div>
  );
};

export default IngredientsAutocomplete;
