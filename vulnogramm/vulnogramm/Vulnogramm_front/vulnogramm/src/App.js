import React, { useState } from 'react';
import './css/App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './commponents/Login';
import Feed from './commponents/Feed';

function App() {


  return (
    <div className="App">

      <BrowserRouter>
        <Routes>
          <Route extract path="/feed" element={<Feed />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
