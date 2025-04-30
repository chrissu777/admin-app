import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RecordingsPage from "./pages/RecordingsPage";
import HomePage from "./pages/HomePage";
import "./App.css";

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/recordings">Recordings</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recordings" element={<RecordingsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
