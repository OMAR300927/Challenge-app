import { useState } from 'react'
import { useNavigate } from "react-router";
import { api } from '../utils/api'

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const register = async(e) => {
    e.preventDefault();
    try {
      await api.post(
        '/users/register',
        {
          username,
          email,
          password
        }
      )
      navigate('/login')
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div className='page-background'>
      <div className='app-container'>
        <div className='auth-content'>
          <h2 className='content-title'>Register</h2>
          <hr className='border-black/50 border-t-2 w-100 mt-8' />
          <form className='form-container' onSubmit={register}>
            <label htmlFor="username" className='label-style'>Username<span className='text-red-500'> *</span></label>
            <input
              id='username'
              type="text"
              placeholder='Enter your username'
              className='form-input'
              onChange={(e) => setUsername(e.target.value)}
            />

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

            <button className='auth-btn'>Register</button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Register

