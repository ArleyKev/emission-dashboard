import React from 'react';
import DashboardPage from './pages/DashboardPages.jsx';
import './styles/base.css';
import './styles/layout.css';
import './styles/components.css';

export default function App() {
  return (
    <div className="app-root" style={{ minHeight: '100vh', position: 'relative' }}>
      <DashboardPage />
      {}
    </div>
  );
}
