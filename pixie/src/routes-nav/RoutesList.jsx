import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import HomePage from '../homepage/HomePage';
import UserAlbum from '../userpage/UserAlbum';
import SignUp from '../auth/SignUp';
import LogIn from '../auth/LogIn';

/**
 *
 */
function RoutesList({ currentUser }) {
  console.debug('RoutesList');

  return (
    <div className='RoutesList'>
      <Routes>
        {!currentUser &&
          <>
            <Route path='/signup' element={<SignUp />} />
            <Route path='/login' element={<LogIn />} />
          </>
        }

        {currentUser &&
        <>
          <Route path='/album' element={<UserAlbum />} />
        </>
        }

        <Route path='/' element={<HomePage />} />
        <Route path='*' element={<Navigate to='/' />} />
      </Routes>
    </div>
  )
}

export default RoutesList;