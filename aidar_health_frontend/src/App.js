import './App.css';
import MainDashboard from './Components/Dashboards/Physicians/MainDashboard';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Components/Login/Login';

function App() {
  return (
    <div className='App'>
        <Router>
              <Routes>
                  <Route path="/login" element={<Login />} />
                  <Route path="/dashboard" element={<MainDashboard />} />
              </Routes>
        </Router>
    </div>
  );
}

export default App;
