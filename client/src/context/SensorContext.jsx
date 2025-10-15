// src/context/SensorContext.jsx
import React, { createContext, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { createSocket } from '../services/websocket';

const SensorContext = createContext(null);

export const SENSOR_LOCATIONS = ['Lab', 'Server Room', 'Storage Room'];
export const SENSOR_TYPES = ['Temperature', 'Humidity'];

export function SensorProvider({ children }) {
  const [selectedLocation, setSelectedLocation] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [wsStatus, setWsStatus] = useState('disconnected'); // 'connected' | 'connecting' | 'disconnected'
  const socketRef = useRef(null);

  const getPreference = () => ({
    location: selectedLocation,
    type: selectedType,
  });

  useEffect(() => {
    setWsStatus('connecting');
    socketRef.current = createSocket({
      url: 'ws://localhost:4000/ws',
      onOpen: () => setWsStatus('connected'),
      onClose: () => setWsStatus('disconnected'),
      onError: () => setWsStatus('disconnected'),
      getPreference,
    });

    return () => {
      socketRef.current?.close();
      socketRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedLocation && selectedType) {
      socketRef.current?.subscribe({ location: selectedLocation, type: selectedType });
    }
  }, [selectedLocation, selectedType]);

  const value = useMemo(
    () => ({
      selectedLocation,
      setSelectedLocation,
      selectedType,
      setSelectedType,
      socket: socketRef.current,
      wsStatus,
    }),
    [selectedLocation, selectedType, wsStatus]
  );

  return <SensorContext.Provider value={value}>{children}</SensorContext.Provider>;
}

export function useSensorContext() {
  const ctx = useContext(SensorContext);
  if (!ctx) throw new Error('useSensorContext must be used within SensorProvider');
  return ctx;
}