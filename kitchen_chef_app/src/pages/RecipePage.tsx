import React from 'react';
import Grid from '@mui/material/Grid';
import {
  Box,
  CircularProgress, Typography,
} from '@mui/material';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import { getRecipe } from '../api/recipes';
import IngredientsCard from '../components/recipe/IngredientsCard';
import NutritionalDataCard from '../components/recipe/NutritionalDataCard';
import Abstract from '../components/recipe/Asbtract';
import Instructions from '../components/recipe/Instructions';

const RecipePage:React.FC = () => {
  const params = useParams();
  const { recipeId } = params;

  const { data: recipe, isLoading } = useQuery(`recipe/${recipeId}`, () => {
    if (typeof recipeId === 'undefined') return undefined;
    return getRecipe(recipeId);
  });

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
      <Grid
        container
        spacing={2}
        paddingY={5}
        style={{
          display: 'grid',
          gridAutoColumns: '1fr',
          gridAutoFlow: 'column',
        }}
      >
        <Grid
          item
          display="flex"
        >
          <IngredientsCard
            ingredients={recipe?.data.ingredients}
            thumbnail={recipe?.data.thumbnail}
          />
        </Grid>
        <Grid item>
          <NutritionalDataCard nutritionalData={nutritionalData} />
          <Box marginY={1} />
          {recipe?.data.instructions ? (
            <Instructions
              instructions={recipe?.data.instructions}
            />
          ) : null}
        </Grid>
      </Grid>
    </Box>
  );
};

export default RecipePage;
