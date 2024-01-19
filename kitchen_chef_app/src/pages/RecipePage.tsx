import React from 'react';
import Grid from '@mui/material/Grid';
import {
  Box,
  Card,
  CardContent, CardMedia, CircularProgress, Typography,
} from '@mui/material';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import RecipeSearchForm from '../form/RecipeSearchForm';
import RecipeCard from '../components/RecipeCard';
import { getRecipe } from '../api/recipes';
import IngredientsCard from '../components/recipe/IngredientsCard';
import NutritionalDataCard from '../components/recipe/NutritionalDataCard';
import Abstract from '../components/recipe/Asbtract';
import Instructions from '../components/recipe/Instructions';

const RecipePage = () => {
  const params = useParams();
  const { recipeId } = params;
  console.log('params', params);

  const { data: recipe, isLoading } = useQuery(`recipe/${recipeId}`, () => getRecipe(recipeId));

  console.log('recipe', recipe);
  if (isLoading || !recipe?.data) return <CircularProgress />;
  const { nutritionalData } = recipe.data;

  return (
    <Box maxWidth="860px" margin="auto">
      <Typography
        component="h1"
        variant="h4"
        sx={{ color: '#181e21' }}
        marginY={7}
      >
        {recipe?.data?.name}
      </Typography>
      {recipe?.data.abstract ? <Abstract abstract={recipe?.data.abstract} /> : null}
      <Grid container spacing={2} paddingY={5}>
        <Grid
          item
          xs={6}
        >
          <IngredientsCard ingredients={recipe?.data.ingredients} thumbnail={recipe?.data.thumbnail} />
        </Grid>
        <Grid item xs={6}>
          <NutritionalDataCard nutritionalData={nutritionalData} />
          <Box marginY={1} />
          {recipe?.data.instructions ? <Instructions instructions={recipe?.data.instructions} /> : null}
        </Grid>
      </Grid>
    </Box>
  );
};

export default RecipePage;
