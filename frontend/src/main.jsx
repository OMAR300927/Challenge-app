import { BrowserRouter, Routes, Route } from "react-router";
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import History from "./components/History.jsx";
import Profile from "./components/Profile.jsx";


createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}/>
      <Route path="/register" element={<Register />}/>
      <Route path="/login" element={<Login />}/>
      <Route path="/history" element={<History />}/>
      <Route path="/profile" element={<Profile />}/>
    </Routes>
  </BrowserRouter>
)
