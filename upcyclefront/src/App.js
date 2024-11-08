import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ImageUpload from './pages/SendPhoto/ImageUpload';
import Home from './pages/Home';
import Identifier from './pages/Identifier';
import Register from './pages/Register';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/register' element={<Register />} />
        <Route path='/identifier' element={<Identifier />} />
        <Route path='/send' element={<ImageUpload />} />
      </Routes>
    </Router>
  );
}

export default App;
