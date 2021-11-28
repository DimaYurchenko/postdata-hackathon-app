import React from 'react';
import {Routes, Route} from 'react-router-dom';
import SimpleMap from './components/SimpleMap';
import './App.css';
import RouteCreator from './components/RouteCreator/RouteCreator';

function App() {
  return (
    <Routes>
      <Route path="/" exact element={<SimpleMap />}/>
      <Route path='/create' exact element={<RouteCreator />}/>
    </Routes>
  );
}

export default App;
