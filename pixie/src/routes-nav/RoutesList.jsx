import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import HomePage from '../homepage/HomePage';
import UserAlbum from '../userpage/UserAlbum';
import SignUpForm from '../auth/SignUpForm';
import LogInForm from '../auth/LogInForm';
import PropTypes from 'prop-types';


/** Site-wide routes.
 *
 */
function RoutesList({ currentUser, signup }) {
  console.debug('RoutesList');

  return (
    <div className='RoutesList'>
      <Routes>
        {!currentUser &&
          <>
            <Route path='/signup' element={<SignUpForm signup={signup} />} />
            <Route path='/login' element={<LogInForm />} />
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

RoutesList.propTypes = {
  currentUser: PropTypes.object,
  signup: PropTypes.func,
}

export default RoutesList;