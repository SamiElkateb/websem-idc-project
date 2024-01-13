import { QueryClient, QueryClientProvider } from 'react-query';
import React from 'react';
import './App.css';
import RecipeListPage from './pages/RecipesListPage';

const App = () => {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <RecipeListPage />
    </QueryClientProvider>
  );
};

export default App;
