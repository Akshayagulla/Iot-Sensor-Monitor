// src/pages/SensorDetails.jsx
import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import Chart from '../components/Chart';
import StatsPanel from '../components/StatsPanel';
import Loader from '../components/Loader';
import PageHeader from '../components/PageHeader';
import { useSensorContext } from '../context/SensorContext';
import { fetchHistoricalData } from '../services/api';

const TYPE_LABEL = {
  Temperature: 'Temperature (°C)',
  Humidity: 'Humidity (%)',
};

export default function SensorDetails() {
  const { location: locParam, type: typeParam } = useParams();
  const location = decodeURIComponent(locParam);
  const type = decodeURIComponent(typeParam);

  const { selectedLocation, setSelectedLocation, selectedType, setSelectedType, socket } =
    useSensorContext();

  const [loading, setLoading] = useState(true);
  const [readings, setReadings] = useState([]);
  const [stats, setStats] = useState({});
  const [error, setError] = useState('');

  // Align context selection with route
  useEffect(() => {
    if (selectedLocation !== location) setSelectedLocation(location);
    if (selectedType !== type) setSelectedType(type);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location, type]);

  // Initial historical fetch
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError('');

    fetchHistoricalData({ location, type })
      .then((data) => {
        console.log(data);
        if (!active) return;
        setReadings(Array.isArray(data.readings) ? data.readings : []);
        setStats(data.stats || {});
        setLoading(false);
      })
      .catch((err) => {
        if (!active) return;
        console.log(err);
        setError('Failed to load historical data.');
        setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [location, type]);

  // Real-time updates: new reading + nested stats every 15s
  useEffect(() => {
    if (!socket) return;

    const handleMessage = (payload) => {
      // Expected payload:
      // { timestamp: "ISO", value: number, stats: { "5min": {...}, "1hr": {...}, "6hr": {...}, "1day": {...} } }
      if (payload?.timestamp !== undefined && payload?.value !== undefined) {
        setReadings((prev) => {
          const next = [...prev, { timestamp: payload.timestamp, value: payload.value }];
          return next.slice(Math.max(0, next.length - 20)); // keep last 20 for line chart
        });
      }
      if (payload?.stats) {
        setStats(payload.stats);
      }
    };

    socket.addListener(handleMessage);
    socket.subscribe({ location, type });

    return () => {
      socket.unsubscribe({ location, type });
      socket.removeListener(handleMessage);
    };
  }, [socket, location, type]);

  const label = useMemo(() => TYPE_LABEL[type] || 'Reading', [type]);

  return (
    <div className="min-h-screen">
      <PageHeader title="Sensor details" subtitle={`${location} — ${type}`} />

      <main className="mx-auto max-w-6xl p-4">
        {loading ? (
          <Loader label="Fetching historical data..." />
        ) : error ? (
          <div className="card border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>
        ) : (
          <div className="grid gap-4 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <Chart readings={readings} label={label} />
            </div>
            <div>
              <StatsPanel stats={stats} unit={type === 'Temperature' ? '°C' : '%'} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}