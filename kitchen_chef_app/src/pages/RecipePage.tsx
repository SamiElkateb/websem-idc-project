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

const RecipePage = () => {
  const params = useParams();
  const { recipeId } = params;
  console.log("params", params);

  const { data: recipe, isLoading } = useQuery(`recipe/${recipeId}`, () => getRecipe(recipeId));

  console.log('recipe', recipe);
  if (isLoading || !recipe?.data) return <CircularProgress />;
  const { nutritionalInformations } = recipe.data;

  return (
    <Box maxWidth="860px" margin="auto">
      <Typography
        component="h1"
        variant="h4"
        sx={{ color: '#181e21' }}
      >
        {recipe?.data?.name}

      </Typography>
      <Grid container spacing={2} paddingY={10}>
        <Grid
          item
          xs={6}
        >
          <IngredientsCard ingredients={recipe?.data.ingredients} thumbnail={recipe?.data.thumbnail} />
        </Grid>
        {/* <Grid item xs={6}> */}
        {/*   <Card sx={{ padding: '1rem' }}> */}
        {/*     <Typography gutterBottom variant="h5" component="h2" noWrap> */}
        {/*       Nutritional Informations */}
        {/*     </Typography> */}
        {/*     <CardContent> */}
        {/*       <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between"> */}
        {/*         <span>Calories </span> */}
        {/*         <span>{`${nutritionalInformations.calories} kCal`}</span> */}
        {/*       </Typography> */}

        {/*       <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between"> */}
        {/*         <span>Sugar </span> */}
        {/*         <span>{`${nutritionalInformations.sugar} g`}</span> */}
        {/*       </Typography> */}
        {/*     </CardContent> */}
        {/*   </Card> */}
        {/* </Grid> */}
      </Grid>
    </Box>
  );
};

export default RecipePage;
