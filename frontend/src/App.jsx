import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import BaseLayout from './components/BaseLayout';
import Form from "./components/Form";
import Recs from "./components/Recs";
import Listings from "./components/Listings";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";
import EditProfile from "./components/EditProfile";


function App() {
  return (
    <AuthProvider>
      <Router>
        <BaseLayout>
          <Routes>
            <Route path="/" element={<Form />} />
            <Route path="/recs" element={<Recs />} />
            <Route path="/listings" element={<Listings />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/edit-profile" element={<EditProfile />} />
          </Routes>
        </BaseLayout>
      </Router>
    </AuthProvider>
  );
}

export default App;
