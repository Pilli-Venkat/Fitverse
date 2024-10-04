// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Register from './pages/Register';
import Login from './pages/Login';

function App() {
  return (
    <Router>
      <Routes>
        {/* Home Page */}
        <Route path="/" element={<Home />} />

        {/* Public Routes */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
