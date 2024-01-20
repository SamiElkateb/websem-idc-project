import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { Button, Grid } from '@mui/material';
import { TAutocompleteIngredient } from '../../models/ingredients';

type IngredientsAutocompleteProps = {
  onAddIngredient: (item: TAutocompleteIngredient) => void
  availableIngredients: TAutocompleteIngredient[]
};

const IngredientsAutocomplete: React.FC<IngredientsAutocompleteProps> = ({
  onAddIngredient,
  availableIngredients,
}) => {
  const [ingredient, setIngredient] = useState<TAutocompleteIngredient>();

  const handleAddClick = () => {
    if (ingredient) {
      onAddIngredient(ingredient);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={9}>
        <Autocomplete
          onChange={(_, newValue) => {
            if (typeof newValue === 'undefined' || newValue === null) return;
            setIngredient(newValue);
          }}
          getOptionLabel={(option) => option.enLabel}
          options={availableIngredients}
          getOptionKey={(option) => option.id}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Ingredient"
              onKeyDown={(e) => {
                if ((e.code === 'Enter' || e.code === 'enter')) {
                  handleAddClick();
                }
              }}
            />
          )}
          size="small"
        />
      </Grid>
      <Grid item xs={3}>
        <Button variant="contained" color="primary" fullWidth onClick={handleAddClick}>
          Add
        </Button>
      </Grid>
    </Grid>
  );
};

export default IngredientsAutocomplete;
