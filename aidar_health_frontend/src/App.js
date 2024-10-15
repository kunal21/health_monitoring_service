import './App.css';
import MainDashboard from './Components/Dashboards/Physicians/MainDashboard';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Components/Login/Login';

function App() {
  return (
    <div className='App'>
        <Router>
              <Routes>
                  <Route path="/" element={<Navigate to="/login" />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/dashboard" element={<MainDashboard />} />
                  <Route path="*" element={<Navigate to="/login" />} />
              </Routes>
        </Router>
    </div>
  );
}

export default App;
