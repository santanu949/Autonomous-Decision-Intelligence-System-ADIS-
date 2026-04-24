import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

export const analyzeData = (data, enableMl = true) =>
  axios.post(`${API}/analyze`, { data, enable_ml: enableMl });

export const simulateScenario = (data, adjustments, name = 'Custom') =>
  axios.post(`${API}/simulate`, { data, adjustments, scenario_name: name });

export const sendChatMessage = (message) =>
  axios.post(`${API}/chat`, { message });

export const getHealth = () => axios.get(`${API}/health`);

export { API, BACKEND_URL };
