import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import RecordingsPage from "./pages/RecordingsPage";
import HomePage from "./pages/HomePage";
import Navbar from "./components/Navbar";
import "./index.css";

function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recordings" element={<RecordingsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
