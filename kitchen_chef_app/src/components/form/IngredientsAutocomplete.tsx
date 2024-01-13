import React, { useMemo, useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { TIngredient } from '../../models/ingredients';

type IngredientsAutocompleteProps = {
  onAddIngredient: (item: string) => void
  availableIngredients: TIngredient[]
};

const IngredientsAutocomplete: React.FC<IngredientsAutocompleteProps> = ({
  onAddIngredient,
  availableIngredients,
}) => {
  const [ingredient, setIngredient] = useState('');
  const options = useMemo(
    () => availableIngredients.map((item) => item.frLabel),
    [availableIngredients],
  );

  const handleAddClick = () => {
    if (ingredient) {
      onAddIngredient(ingredient);
      setIngredient('');
    }
  };

  return (
    <div>
      <Autocomplete
        value={ingredient}
        onChange={(event, newValue) => {
          setIngredient(newValue);
        }}
        options={options}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Ingredient"
            onKeyDown={(e) => {
              if ((e.code === 'Enter' | e.code == 'enter') && e.target.value) {
                handleAddClick(e.target.value);
                setIngredient('');
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
