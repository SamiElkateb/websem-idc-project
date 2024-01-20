import React, { useEffect, useState } from 'react';
import Grid from '@mui/material/Grid';
import { Box, CircularProgress } from '@mui/material';
import RecipeSearchForm from '../form/RecipeSearchForm';
import RecipeCard from '../components/RecipeCard';
import { TRecipe } from '../models/recipes';
import { getRecipes } from '../api/recipes';

const RecipeListPage = () => {
  const [recipes, setRecipes] = useState<TRecipe[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const handleUpdateRecipes = (newRecipes:TRecipe[]) => {
    setRecipes(newRecipes);
    setIsLoading(false);
  };

  useEffect(() => {
    getRecipes({ filteringIngredients: [], recipeFilters: [], recipeSearchTitle: '' }).then(({ data }) => {
      handleUpdateRecipes(data);
    });
  }, []);

  return (
    <>
      <RecipeSearchForm onUpdateRecipes={handleUpdateRecipes} />
      <Grid container spacing={2} paddingY={10}>
        {isLoading ? <Box margin="auto"><CircularProgress /></Box> : recipes.map((recipe) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={recipe.id}>
            <RecipeCard title={recipe?.name} description={recipe?.instructions} thumbnail={recipe?.thumbnail} uri={recipe?.id} />
          </Grid>
        ))}
      </Grid>
    </>
  );
};

export default RecipeListPage;
