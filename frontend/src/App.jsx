import "./App.css";
import Form from "./components/Form";
import Recs from "./components/Recs";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
        <Router>
          <Routes>
            <Route path="/" element={<Form />} />
            <Route path="/recs" element={<Recs />} />
          </Routes>
        </Router>
  );
}

export default App;
