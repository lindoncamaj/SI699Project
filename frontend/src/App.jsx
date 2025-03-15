import "./App.css";
import Form from "./components/Form";
import Recs from "./components/Recs";
import Listings from "./components/Listings";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
        <Router>
          <Routes>
            <Route path="/" element={<Form />} />
            <Route path="/recs" element={<Recs />} />
            <Route path="/listings" element={<Listings />} />
          </Routes>
        </Router>
  );
}

export default App;
