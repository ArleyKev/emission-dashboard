import React, { useMemo } from 'react';
import {
  ResponsiveContainer, AreaChart, XAxis, YAxis, Tooltip, Area, Legend
} from 'recharts';

const COLORS = ['#2b6cb0','#f6ad55','#9f7aea','#48bb78','#e53e3e','#63b3ed'];

export default function TimeSeriesChart({ timeSeries = [] }) {
  const keys = useMemo(() => {
    if (!timeSeries || !timeSeries.length) return [];
    return Object.keys(timeSeries[0]).filter(k => k !== 'year');
  }, [timeSeries]);

  return (
    <div style={{ width: '100%', height: 360 }}>
      <ResponsiveContainer>
        <AreaChart data={timeSeries}>
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip formatter={(value) => new Intl.NumberFormat().format(value)} />
          <Legend />
          {keys.map((key, idx) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stackId="1"
              stroke={COLORS[idx % COLORS.length]}
              fill={COLORS[idx % COLORS.length]}
              fillOpacity={0.8}
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
