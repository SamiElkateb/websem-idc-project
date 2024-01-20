import { QueryClient, QueryClientProvider } from 'react-query';
import React from 'react';
import './App.css';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';
import { Container } from '@mui/material';
import RecipeListPage from './pages/RecipesListPage';
import RecipePage from './pages/RecipePage';
import Header from './components/Header';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RecipeListPage />,
  },
  {
    path: 'recipes/:recipeId',
    element: <RecipePage />,
  },
]);

const App:React.FC = () => {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <Header />
      <Container maxWidth="md">
        <RouterProvider router={router} />
      </Container>
    </QueryClientProvider>
  );
};

export default App;
