import "./App.css";
import Form from "./components/Form";
import Recs from "./components/Recs";
import Listings from "./components/Listings";
import Login from "./components/Login";
import Register from "./components/Register";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Avatar from "./components/Avatar"; 
import EditProfile from "./components/EditProfile";
function App() {
  return (
        <Router>
        <Avatar />
          <Routes>
            <Route path="/" element={<Form />} />
            <Route path="/recs" element={<Recs />} />
            <Route path="/listings" element={<Listings />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/edit-profile" element={<EditProfile />} />
          </Routes>
        </Router>
  );
}

export default App;
