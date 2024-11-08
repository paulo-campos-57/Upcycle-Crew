import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Identifier from './pages/Identifier';
import Register from './pages/Register';
import Camera from './pages/Camera';
import Keyboard from './pages/Keyboard/index.js';
import Recieved from './pages/Recieved/index.js';
import Discard from './pages/Discard/index.js';
import EndPage from './pages/end/index.js';

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
        <Route path='/recieved' element={<Recieved />} />
        <Route path='/discard' element={<Discard/>}/>
        <Route path='/end' element={<EndPage/>}/>
      </Routes>
    </Router>
  );
}

export default App;
