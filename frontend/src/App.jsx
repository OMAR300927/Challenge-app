import ChallengeGenerator from "./components/ChallengeGenerator"
import Navbar from "./components/Navbar"
import { useEffect } from "react";
import { useNavigate } from "react-router";
import { api } from "./utils/api";

function App() {
  const navigate = useNavigate()

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await api.get("/users/me");
      } catch (error) {
        if (error.response?.status === 401) {
          navigate("/login");
        }
      }
    };

    checkAuth();
  }, [navigate]);

  return (
    <div className="page-background relative">
      <Navbar />
      <ChallengeGenerator />
    </div>
  )
}

export default App
