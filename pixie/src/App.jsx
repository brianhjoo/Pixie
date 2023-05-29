import React, { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import NavBar from './routes-nav/NavBar';
import RoutesList from './routes-nav/RoutesList';

function App() {
  const [currentUser, setCurrentUser] = useState({
    data: null,
    isLoading: true,
    errors: null,
  });

  return (
    <BrowserRouter>
      <NavBar currentUser={currentUser.data} />
      <RoutesList currentUser={currentUser.data} />
    </BrowserRouter>
  );
}

export default App;