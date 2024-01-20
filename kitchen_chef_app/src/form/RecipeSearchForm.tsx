import React, { useEffect, useState } from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import { Button } from '@mui/material';
import { useQuery } from 'react-query';
import RecipeSearchBar from '../components/form/RecipeSearchBar';
import IngredientsAutocomplete from '../components/form/IngredientsAutocomplete';
import Filters from '../components/form/Filters';
import { getIngredients } from '../api/ingredients';
import { TAutocompleteIngredient } from '../models/ingredients';
import { getRecipeFilters, getRecipes } from '../api/recipes';
import { TRecipe } from '../models/recipes';
import { TFilter } from '../models/others';

type TRecipeSearchFormProps = {
  onUpdateRecipes: (recipes:TRecipe[]) => void
};

const RecipeSearchForm:React.FC<TRecipeSearchFormProps> = ({ onUpdateRecipes }) => {
  const [recipeFilters, setRecipeFilters] = useState<TFilter[]>([]);
  const [recipeSearchTitle, setRecipeSearchTitle] = useState<string>('');

  useEffect(() => {
    getRecipeFilters().then((resfilters) => {
      setRecipeFilters(resfilters.data.map(((item) => ({ ...item, active: false }))).sort());
    });
  }, []);

  const { data: availableIngredients } = useQuery('ingredients', getIngredients);

  const [filteringIngredients, setFilteringIngredients] = useState<TAutocompleteIngredient[]>([]);

  const handleChangeRecipeSearchTitle = (searchTitle:string) => {
    setRecipeSearchTitle(searchTitle);
  };
  const handleAddIngredient = (ingredient: TAutocompleteIngredient) => {
    setFilteringIngredients((prevState) => [...prevState, ingredient]);
  };
  const handleRemoveIngredient = (ingredient: string) => {
    setFilteringIngredients((prevState) => prevState.filter((item) => item.id !== ingredient));
  };
  const handleActivateFilter = (filterName: TFilter) => {
    setRecipeFilters(
      (prevState) => prevState.map((item) => (item === filterName
        ? { ...item, active: true }
        : item)),
    );
  };
  const handleDeactivateFilter = (filterName: TFilter) => {
    setRecipeFilters((prevState) => prevState.map((item) => (item === filterName
      ? { ...item, active: false }
      : item)));
  };

  const handleFormSubmit = async () => {
    const recipes = await getRecipes({ filteringIngredients, recipeFilters, recipeSearchTitle });
    onUpdateRecipes(recipes.data);
  };

  return (
    <Container>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <RecipeSearchBar
            searchTitle={recipeSearchTitle}
            onSearchTitleChange={handleChangeRecipeSearchTitle}
          />
        </Grid>
        <Grid item xs={12}>
          <IngredientsAutocomplete
            onAddIngredient={handleAddIngredient}
            availableIngredients={availableIngredients?.data || []}
          />
        </Grid>
        <Grid item xs={12}>
          <Filters
            filters={recipeFilters}
            ingredients={filteringIngredients}
            onActivateFilter={handleActivateFilter}
            onDeactiveFilter={handleDeactivateFilter}
            onRemoveIngredient={handleRemoveIngredient}
          />
        </Grid>
        <Grid item xs={5} />
        <Grid item xs={2}>
          <Button variant="contained" color="primary" fullWidth onClick={handleFormSubmit}>
            Send
          </Button>
        </Grid>
        {/* <Grid item xs={6}> */}
        {/*   <DietaryCheckboxes /> */}
        {/* </Grid> */}
      </Grid>
    </Container>
  );
};

export default RecipeSearchForm;
