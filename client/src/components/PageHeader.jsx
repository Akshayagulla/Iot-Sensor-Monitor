import React from 'react';
import { Link } from 'react-router-dom';

export default function PageHeader({ title, subtitle }) {
  return (
    <header className="sticky top-0 z-10 border-b border-gray-200 bg-white/90 backdrop-blur">
      <div className="mx-auto max-w-6xl p-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <span className="h-8 w-8 flex items-center justify-center rounded-xl bg-brand text-white font-bold">IoT</span>
            <span className="text-lg font-semibold text-gray-900">Dashboard</span>
          </Link>
          <div className="text-xs text-gray-500">Real-time monitoring</div>
        </div>
        <div className="mt-4">
          <h1 className="text-xl font-semibold text-gray-900">{title}</h1>
          {subtitle && <p className="mt-1 text-sm text-gray-600">{subtitle}</p>}
        </div>
      </div>
    </header>
  );
}