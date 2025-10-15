import React from 'react';
import { Link } from 'react-router-dom';

export default function SensorList({ sensors }) {
  if (!sensors?.length) {
    return <div className="text-center text-sm text-gray-500 py-8">No sensors match the current selection.</div>;
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {sensors.map((s) => {
        const id = `${s.location}-${s.type}`.toLowerCase().replace(/\s+/g, '-');
        return (
          <Link
            key={id}
            to={`/sensor/${encodeURIComponent(s.location)}/${encodeURIComponent(s.type)}`}
            className="block rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow-md transition"
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs text-gray-500">Location</div>
                <div className="text-sm font-semibold">{s.location}</div>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-500">Type</div>
                <div className="text-sm font-semibold">{s.type}</div>
              </div>
            </div>
            <div className="mt-3 text-xs text-gray-500">Click to view details</div>
          </Link>
        );
      })}
    </div>
  );
}