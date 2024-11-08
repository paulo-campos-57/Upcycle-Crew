import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Identifier from './pages/Identifier';
import Register from './pages/Register';
import Camera from './pages/Camera/index.tsx';
import Keyboard from './pages/Keyboard/index.js';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Register />} />
        <Route path='/begin' element={<Home />} />
        <Route path='/identifier' element={<Identifier />} />
        <Route path='/insert-cpf' element={<Keyboard />}/>
        <Route path='/camera' element={<Camera />} />
        <Route path='/keyboard' element={<Keyboard />} />
      </Routes>
    </Router>
  );
}

export default App;
