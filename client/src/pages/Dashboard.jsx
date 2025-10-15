// src/pages/Dashboard.jsx
import React, { useMemo } from 'react';
import Dropdown from '../components/Dropdown';
import SensorList from '../components/SensorList';
import PageHeader from '../components/PageHeader';
import { useSensorContext, SENSOR_LOCATIONS, SENSOR_TYPES } from '../context/SensorContext';

/**
 * Dynamic filtering logic:
 * - Only Location selected → show all types for that location
 * - Only Type selected → show all locations with that type
 * - Both selected → show only that specific sensor
 * Demo assumes both sensors exist in all locations.
 */
export default function Dashboard() {
  const {
    selectedLocation,
    setSelectedLocation,
    selectedType,
    setSelectedType,
    wsStatus,
  } = useSensorContext();

  const sensors = useMemo(() => {
    if (!selectedLocation && !selectedType) {
      return SENSOR_LOCATIONS.flatMap((loc) => SENSOR_TYPES.map((t) => ({ location: loc, type: t })));
    }
    if (selectedLocation && !selectedType) {
      return SENSOR_TYPES.map((t) => ({ location: selectedLocation, type: t }));
    }
    if (!selectedLocation && selectedType) {
      return SENSOR_LOCATIONS.map((loc) => ({ location: loc, type: selectedType }));
    }
    return [{ location: selectedLocation, type: selectedType }];
  }, [selectedLocation, selectedType]);

  return (
    <div className="min-h-screen">
      <PageHeader title="IoT Sensor Monitoring" subtitle="Real-time dashboard with filtering and live updates" />

      <main className="mx-auto max-w-6xl p-4">
        <div className="card p-4 mb-4">
          <div className="grid gap-3 sm:grid-cols-3">
            <Dropdown
              label="Location"
              options={SENSOR_LOCATIONS}
              value={selectedLocation}
              onChange={setSelectedLocation}
            />
            <Dropdown
              label="Sensor type"
              options={SENSOR_TYPES}
              value={selectedType}
              onChange={setSelectedType}
            />
            <div>
              <div className="text-xs text-slate-500">WebSocket</div>
              <div
                className={`pill mt-1 ${
                  wsStatus === 'connected'
                    ? 'border-green-200 bg-green-50 text-green-700'
                    : wsStatus === 'connecting'
                    ? 'border-yellow-200 bg-yellow-50 text-yellow-700'
                    : 'border-slate-200 bg-slate-50 text-slate-700'
                }`}
              >
                Status: {wsStatus}
              </div>
            </div>
          </div>
        </div>

        <SensorList sensors={sensors} />
      </main>
    </div>
  );
}