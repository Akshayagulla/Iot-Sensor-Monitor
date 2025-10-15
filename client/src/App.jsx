import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SensorProvider } from './context/SensorContext';
import Dashboard from './pages/Dashboard';
import SensorDetails from './pages/SensorDetails';

export default function App() {
  return (
    <SensorProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sensor/:location/:type" element={<SensorDetails />} />
        </Routes>
      </BrowserRouter>
    </SensorProvider>
  );
}