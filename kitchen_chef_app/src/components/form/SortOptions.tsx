import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';

import React from 'react';

function SortOptions() {
  return (
    <FormControl fullWidth size="small">
      <InputLabel>Tri des recettes</InputLabel>
      <Select
        label="Tri des recettes"
      >

        <MenuItem value="kcal">Kcal</MenuItem>
        <MenuItem value="missing">Ingrédients manquants</MenuItem>
        <MenuItem value="transformed">Ingrédients transformés</MenuItem>
      </Select>
    </FormControl>
  );
}

export default SortOptions;
