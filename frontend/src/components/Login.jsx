import { useState } from 'react'
import { useNavigate } from "react-router";
import { api } from '../utils/api'

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');


  const navigate = useNavigate();

  const login = async (e) => {
    e.preventDefault();

    let hasError = false;

    if (!email) {
      setEmailError('email is required');
      hasError = true;
    } else if (email.split('@')[0].length < 3) {
      setEmailError('the part before @ must be at least 3 characters');
      hasError = true;
    }


    if (!password) {
      setPasswordError('password is required');
      hasError = true;
    } else if (password.length < 8) {
      setPasswordError('password must be at least 8 characters');
      hasError = true;
    }

    if (hasError) {
      return;
    }

    try {
      setError(null);

      await api.post(
        '/users/login',
        {
          email,
          password
        }
      )
      navigate('/')
    } catch (e) {
      setError(e.response?.data?.detail);
    }
  }

  return (
    <div className='page-background'>
      <div className='app-container'>
        <div className='auth-content'>
          <h2 className='content-title'>Login</h2>
          <hr className='border-black/50 border-t-2 w-100 mt-8' />
          <form className='form-container' onSubmit={login}>
            <label htmlFor="email" className='label-style'>Email<span className='text-red-500'> *</span></label>
            <input
              id='email'
              type="email"
              placeholder='Enter your email'
              className={`form-input ${!emailError && 'mb-6'}`}
              onChange={(e) => {
                setEmail(e.target.value);
                setEmailError('');
              }}
            />
            {emailError && (
              <label className='input-error-msg'>{emailError}</label>
            )}

            <label htmlFor="password" className='label-style'>Password<span className='text-red-500'> *</span></label>
            <input
              id='password'
              type="password"
              placeholder='Enter your password'
              className={`form-input ${!passwordError && 'mb-6'}`}
              onChange={(e) => {
                setPassword(e.target.value);
                setPasswordError('');
              }}
            />
            {passwordError && (
              <label className='input-error-msg'>{passwordError}</label>
            )}

            <button type='submit' className='auth-btn'>Login</button>
            {error && (
              <label className='input-error-msg'>{error}</label>
            )}
            <button type='button' className='auth-btn mt-5' onClick={() => navigate('/register')}>Register</button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login