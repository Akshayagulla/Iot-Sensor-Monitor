import React from 'react';

const blocks = [
  { key: '5min', label: 'Last 5 min' },
  { key: '1hr', label: 'Last 1 hr' },
  { key: '6hr', label: 'Last 6 hr' },
  { key: '1day', label: 'Last 24 hr' },
];

export default function StatsPanel({ stats = {}, unit = '' }) {
  const fmt = (v) => (v === null || v === undefined ? '—' : `${v}${unit}`);

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <div className="mb-2 text-sm font-semibold">Statistics</div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {blocks.map((b) => {
          const s = stats[b.key] || {};
          return (
            <div key={b.key} className="rounded-lg bg-gray-50 p-3 border border-gray-200">
              <div className="text-xs text-gray-500">{b.label}</div>
              <div className="mt-2 grid grid-cols-3 gap-2 text-sm">
                <div>
                  <div className="text-xs text-gray-500">Min</div>
                  <div className="font-semibold">{fmt(s.min)}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500">Avg</div>
                  <div className="font-semibold">{fmt(s.avg)}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500">Max</div>
                  <div className="font-semibold">{fmt(s.max)}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}