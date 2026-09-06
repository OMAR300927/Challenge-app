import { useState } from 'react'
import { useNavigate } from "react-router";
import { api } from '../utils/api'

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const login = async(e) => {
    e.preventDefault();
    try {
      await api.post(
        '/users/login',
        {
          email,
          password
        }
      )
      navigate('/')
    } catch (e) {
      console.log(e)
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
              type="text"
              placeholder='Enter your email'
              className='form-input'
              onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password" className='label-style'>Password<span className='text-red-500'> *</span></label>
            <input
              id='password'
              type="password"
              placeholder='Enter your password'
              className='form-input'
              onChange={(e) => setPassword(e.target.value)}
            />

            <button className='auth-btn'>Login</button>
            <button className='auth-btn mt-5' onClick={() => navigate('/register')}>Register</button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login