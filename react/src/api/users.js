import instance from './axios';
import { getToken } from '../utils/auth';

export const getOnlineUsers = async () => {
  const token = getToken();
  const response = await instance.get('/api/users/online', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};

export const sendHeartbeat = async () => {
  const token = getToken();
  const response = await instance.post('/api/users/heartbeat', {}, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
