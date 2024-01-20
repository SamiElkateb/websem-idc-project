import TextField from '@mui/material/TextField';
import React from 'react';

const RecipeSearchBar = ({ searchTitle, onSearchTitleChange }) => {
  const handleSearchTitleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onSearchTitleChange(event.target.value);
  };
  return (
    <TextField
      label="Recherche par nom des recettes"
      variant="outlined"
      fullWidth
      size="small"
      value={searchTitle}
      onChange={handleSearchTitleChange}
    />
  );
};

export default RecipeSearchBar;
