import React from 'react';
import { Link, NavLink } from 'react-router-dom';


/** Navigation Bar
 *
 * Props:
 *
 * State:
 *
 * App -> NavBar
 */
function NavBar({ currentUser }) {
  console.debug('NavBar');

  /** Navigation to use when user is logged out */
  function loggedOutNav() {
    return (
      <ul className='loggedOutNav flex'>
        <li>
          <NavLink to='/signup'>
            Sign Up
          </NavLink>
        </li>
        <li>
          <NavLink to='/login'>
            Log In
          </NavLink>
        </li>
      </ul>
    );
  }

  /** Navigation to use when user is logged in */
  function loggedInNav() {
    return (
      <ul className='loggedInNav flex'>
        <li>
          <NavLink to='/'>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to='album'>
            Your Album
          </NavLink>
        </li>
        <li>
          <Link to='/'>
            Log Out
          </Link>
        </li>
      </ul>
    );
  }

  return (
    <nav className='NavBar flex justify-between m-2'>
      <Link to='/' class="text-3xl">
        pixie
      </Link>
      { currentUser ? loggedInNav() : loggedOutNav() }
    </nav>
  );
}

export default NavBar;