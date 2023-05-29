import React, { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import NavBar from './routes-nav/NavBar';
import RoutesList from './routes-nav/RoutesList';
import PixieAPI from './api/api';

function App() {
  const [currentUser, setCurrentUser] = useState({
    data: null,
    isLoading: true,
    errors: null,
  });

  /** Handles site-wide signup.
   *
   */
  async function signup(signupData) {
    const userData = await PixieAPI.signup(signupData);

    setCurrentUser({
      data: userData,
      isLoading: false,
      errors: null,
    });
  }

  return (
    <BrowserRouter>
      <NavBar currentUser={currentUser.data} />
      <RoutesList currentUser={currentUser.data} signup={signup} />
    </BrowserRouter>
  );
}

export default App;