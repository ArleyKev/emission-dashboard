import { useState, useEffect } from 'react';
import api from '../api/apiClient';

export default function useEmissions({ startYear, endYear, sector, region } = {}) {
  const [data, setData] = useState({ time_series: [], loading: true, error: null });

  useEffect(() => {
    let cancelled = false;
    async function fetchData() {
      setData(d => ({ ...d, loading: true, error: null }));
      try {
        const params = {};
        if (startYear) params.start_year = startYear;
        if (endYear) params.end_year = endYear;
        if (sector) params.sector = sector;
        if (region) params.region = region;
        const res = await api.get('/emissions', { params });
        console.log('API /emissions response', res && res.data);
        if (!cancelled) setData({ time_series: res.data.time_series || [], loading: false, error: null });
      } catch (err) {
        if (!cancelled) setData({ time_series: [], loading: false, error: err.message || err.toString() });
      }
    }
    fetchData();
    return () => { cancelled = true; };
  }, [startYear, endYear, sector, region]);

  return data;
}
