import TextField from '@mui/material/TextField';
import React from 'react';

type TRecipeSearchBar = {
  searchTitle: string;
  onSearchTitleChange: (value: string) => void;
};
const RecipeSearchBar:React.FC<TRecipeSearchBar> = ({ searchTitle, onSearchTitleChange }) => {
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
