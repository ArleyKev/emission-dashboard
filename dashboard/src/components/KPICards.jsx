import React from 'react';

function formatNumber(n) {
  return Intl.NumberFormat().format(Math.round(n));
}

export default function KPICards({ timeSeries = [] }) {
  const latest = timeSeries.length ? timeSeries[timeSeries.length - 1] : null;
  const total = latest ? Object.entries(latest)
    .filter(([k]) => k !== 'year')
    .reduce((s, [,v]) => s + (v||0), 0) : 0;

  let yoy = null;
  if (timeSeries.length >= 2) {
    const last = timeSeries[timeSeries.length - 1];
    const prev = timeSeries[timeSeries.length - 2];
    const lastTotal = Object.entries(last).filter(([k])=>k!=='year').reduce((s,[,v])=>s+(v||0),0);
    const prevTotal = Object.entries(prev).filter(([k])=>k!=='year').reduce((s,[,v])=>s+(v||0),0);
    yoy = prevTotal ? ((lastTotal - prevTotal) / prevTotal) * 100 : null;
  }

  return (
    <div style={{display:'flex', gap:16, marginBottom:16}}>
      <div className="kp-card" style={{flex:1}}>
        <div className="kp-card-title">Total emissions (latest)</div>
        <div className="kp-card-value" style={{fontSize:22, fontWeight:700}}>{formatNumber(total)} tCO2e</div>
      </div>
      <div className="kp-card" style={{width:200}}>
        <div className="kp-card-title">YoY</div>
        <div className="kp-card-value" style={{fontSize:18, fontWeight:600}}>
          {yoy===null ? '—' : `${yoy>0?'+':''}${yoy.toFixed(1)}%`}
        </div>
      </div>
      <div className="kp-card" style={{width:200}}>
        <div className="kp-card-title">Years</div>
        <div className="kp-card-value">{timeSeries.length ? `${timeSeries[0].year} — ${timeSeries[timeSeries.length-1].year}` : '—'}</div>
      </div>
    </div>
  );
}
