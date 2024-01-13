import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import { Button } from '@mui/material';
import { useQuery } from 'react-query';
import RecipeSearchBar from '../components/form/RecipeSearchBar';
import SortOptions from '../components/form/SortOptions';
import IngredientsAutocomplete from '../components/form/IngredientsAutocomplete';
import Filters from '../components/form/Filters';
import { getIngredients } from '../api/ingredients';
import { TIngredient } from '../models/ingredients';
import { getRecipes } from '../api/recipes';
import { TRecipe } from '../models/recipes';
import { TFilter } from '../models/others';

type TRecipeSearchFormProps = {
  onUpdateRecipes: (recipes:TRecipe[]) => void
};

const RecipeSearchForm:React.FC<TRecipeSearchFormProps> = ({ onUpdateRecipes }) => {
  const [filters, setFilters] = useState([{ name: 'Gluten-Free', active: false },
    { name: 'Vegan', active: false },
    { name: 'Dairy-Free', active: false }].sort());

  const { data: availableIngredients } = useQuery('ingredients', getIngredients);

  const [filteringIngredients, setFilteringIngredients] = useState<TIngredient[]>([]);

  const handleAddIngredient = (ingredient: TIngredient) => {
    setFilteringIngredients((prevState) => [...prevState, ingredient]);
  };
  const handleRemoveIngredient = (ingredient: string) => {
    setFilteringIngredients((prevState) => prevState.filter((item) => item.id !== ingredient));
  };
  const handleActivateFilter = (filterName: TFilter) => {
    setFilters(
      (prevState) => prevState.map((item) => (item === filterName
        ? { ...item, active: true }
        : item)),
    );
  };
  const handleDeactivateFilter = (filterName: TFilter) => {
    setFilters((prevState) => prevState.map((item) => (item === filterName
      ? { ...item, active: false }
      : item)));
  };

  const handleFormSubmit = async () => {
    const recipes = await getRecipes({ filteringIngredients });
    onUpdateRecipes(recipes.data);
  };

  return (
    <Container>
      <Grid container spacing={2}>
        <Grid item xs={9}>
          <RecipeSearchBar />
        </Grid>
        <Grid item xs={3}>
          <SortOptions />
        </Grid>
        <Grid item xs={9}>
          <IngredientsAutocomplete
            onAddIngredient={handleAddIngredient}
            availableIngredients={availableIngredients?.data || []}
          />
        </Grid>
        <Grid item xs={3}>
          <Button variant="contained" color="primary" fullWidth>
            Add
          </Button>
        </Grid>
        <Grid item xs={12}>
          <Filters
            filters={filters}
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
