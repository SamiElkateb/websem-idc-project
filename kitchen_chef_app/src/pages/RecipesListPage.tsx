import React, { useState } from 'react';
import { Box } from '@mui/material';
import RecipeSearchForm from '../form/RecipeSearchForm';
import RecipeCard from '../components/RecipeCard';
import { TRecipe } from '../models/recipes';

const RecipeListPage = () => {
  const [recipes, setRecipes] = useState<TRecipe[]>([]);
  const handleUpdateRecipes = (newRecipes:TRecipe[]) => {
    setRecipes(newRecipes);
  };

  return (
    <>
      <RecipeSearchForm onUpdateRecipes={handleUpdateRecipes} />
      <Box paddingY={10}>
        {recipes.map((recipe) => (
          <RecipeCard title={recipe?.name} description={recipe?.instructions} />
        ))}
      </Box>
    </>
  );
};

export default RecipeListPage;
