import React, { useState } from 'react';
import Grid from '@mui/material/Grid';
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
      <Grid container spacing={2} paddingY={10}>
        {recipes.map((recipe) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={recipe.id}>
            <RecipeCard title={recipe?.name} description={recipe?.instructions} thumbnail={recipe?.thumbnail} uri={recipe?.id} />
          </Grid>
        ))}
      </Grid>
    </>
  );
};

export default RecipeListPage;
