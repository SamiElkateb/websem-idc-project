import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { Button, Container, Grid } from '@mui/material';
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
    <Grid container spacing={2}>
      <Grid item xs={9}>
        <Autocomplete
          onChange={(_, newValue) => {
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
                if ((e.code === 'Enter' || e.code === 'enter') && e.target.value) {
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
