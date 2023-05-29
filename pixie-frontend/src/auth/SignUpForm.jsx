import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';


/** Signup form.
 *
 * Props:
 *  signup - parent function to call.
 *
 * State:
 *  formData - {username, password, firstName, lastName, email}
 *  formErrors - array of errors
 *
 * RoutesList -> SignUpForm
 */
function SignUpForm({ signup }) {
  console.debug('SignUpForm');

  const [formData, setFormData] = useState({
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    email: '',
  });
  const [formErrors, setFormErrors] = useState([]);
  const navigate = useNavigate();

  /** Handle form submission */
  async function handleSubmit(evt) {
    evt.preventDefault();
    try {
      await signup(formData);
      navigate('/album');
    } catch(err) {
      setFormErrors(err);
    }
  }

  /** Handle form data field */
  function handleChange(evt) {
    const { name, value } = evt.target;
    setFormData(data => ({
      ...data,
      [name]: value,
    }));
  }

  return (
    <div className='SignUpForm flex flex-col items-center'>
      <h2 className='uppercase'>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            name='username'
            placeholder='username'
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            name='password'
            placeholder='password'
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            name='firstName'
            placeholder='firstname'
            value={formData.firstName}
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            name='lastName'
            placeholder='lastname'
            value={formData.lastName}
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            name='email'
            placeholder='email'
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <button className='uppercase border rounded-md px-2 mt-2 bg-teal-200'>
          Submit
        </button>
      </form>
    </div>
  );
}

SignUpForm.propTypes = {
  signup: PropTypes.func,
}

export default SignUpForm;