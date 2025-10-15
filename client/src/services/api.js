// src/services/api.js
import axios from 'axios';

/**
 * Axios setup for REST calls.
 * REACT_APP_API_BASE_URL should point to your backend (e.g., http://localhost:4000).
 */
const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 12000,
});

/**
 * Fetch historical data for a sensor {location, type}.
 * Expected response shape (based on your sample):
 * {
 *   sensor_id: "4",
 *   readings: [{ timestamp: "ISO", value: number }, ...],
 *   stats: {
 *     "5min": { min, max, avg },
 *     "1hr": { min, max, avg },
 *     "6hr": { min, max, avg },
 *     "1day": { min, max, avg }
 *   }
 * }
 */
export const fetchHistoricalData = async({ location, type }) => {
    const res = await api.get('/api/v1/readings/historical', {
        params: { location, type },
    });
    return res.data;
};

export default api;