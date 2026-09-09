import { ArrowLeft } from "lucide-react";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router";
import { api } from '../utils/api'

const Profile = () => {
  const [username, setUsername] = useState('');
  const [profileImage, setProfileImage] = useState(null);

  const navigate = useNavigate();

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

  useEffect(() => {
    const getUsername = async () => {
      try {
        const response = await api.get('/users/username')

        setUsername(response.data)
      } catch (e) {
        console.log(e)
      }
    }

    getUsername();
  }, [])

  const changeUsername = async () => {
    try {
      const response = await api.post(
        '/users/change-username',
        {
          username: username
        }
      )
      setUsername(response.data)
    } catch (e) {
      console.log(e.response?.data)
    }
  }

  const logout = async () => {
    try {
      const response = await api.post(
        '/users/logout'
      )
      navigate('/login')
      console.log(response.data)
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div className="page-background">
      <div className="profile-container">
        <Link to='/'>
          <ArrowLeft size={40} strokeWidth={3} className="text-gray-200 m-3 cursor-pointer transition duration-300 hover:scale-110 hover:text-white active:scale-103" />
        </Link>
        <div className="flex flex-col items-center justify-center">
          <img
            src={profileImage || '/default-image.png'}
            alt='profile-picture'
            className='w-50 h-50 md:w-60 md:h-60 rounded-full object-cover'
          />
          <div className="mt-30">
            <div className="flex flex-col">
              <label htmlFor="username" className="label-style text-gray-100 font-semibold">Username <span className="text-red-600">*</span></label>
              <div className="flex items-center gap-4">
                <input
                  type="text"
                  name="username"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="text-gray-200 text-xl sm:text-2xl md:text-3xl border-2 p-2 rounded-2xl"
                />

                <button
                  onClick={changeUsername}
                  className="profile-btn"
                >
                  Update
                </button>
              </div>
            </div>
            <div className="mt-30 flex items-center justify-center">
              <button
                className="profile-btn w-100 sm:w-120 md:w-140 mx-3"
                onClick={logout}  
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile