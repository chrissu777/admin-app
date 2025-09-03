import { BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom";
import RecordingsPage from "./pages/RecordingsPage";
import LoginPage from "./pages/LoginPage";
import Navbar from "./components/Navbar";
import PrivateRoute from "./components/PrivateRoute";
import { AuthProvider } from "./contexts/AuthContext";
import "./index.css";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div>
          <Navbar />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route 
              path="/" 
              element={
                <PrivateRoute>
                  <Navigate to="/recordings" replace />
                </PrivateRoute>
              } 
            />
            <Route 
              path="/recordings" 
              element={
                <PrivateRoute>
                  <RecordingsPage />
                </PrivateRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
