import { Link } from 'react-router'
import {api} from '../utils/api'
import { useState, useEffect } from 'react';

const Navbar = () => {
  const [profileImage, setProfileImage] = useState(null);

  useEffect(() => {
    const getProfileImage = async () => {
      try {
        const response = await api.get('/users/get-image')

        setProfileImage(response.data)
      } catch (e) {
        console.log(e)
      }
    }

    getProfileImage()
  }, [])

  return (
    <div className="absolute w-full h-20 top-0 z-50 flex items-center justify-between bg-indigo-900/30 px-8">
      <Link
        className="text-gray-200 text-lg sm:text-xl md:text-2xl font-bold cursor-pointer"
        to='/'
      >
        Challenge Application
      </Link>
      <div className="flex items-center gap-6 text-gray-200 text-base sm:text-lg md:text-xl lg:text-2xl font-semibold">
        <Link to='/history'>History</Link>
        <Link to='/profile'>
          <img
          src={profileImage || '/default-image.png'}
          alt='profile-picture'
          className='w-10 h-10 rounded-full object-cover cursor-pointer'
        />
        </Link>
      </div>
    </div>
  )
}

export default Navbar