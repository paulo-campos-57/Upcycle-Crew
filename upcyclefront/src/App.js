import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ImageUpload from './pages/SendPhoto/ImageUpload';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/send' element={<ImageUpload />} />
      </Routes>
    </Router>
  );
}

export default App;
