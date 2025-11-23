import instance from './axios';
import { getToken } from '../utils/auth';

export const getProfile = async () => {
  const token = getToken();
  const response = await instance.get('/api/profile', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};

export const updateProfile = async (full_name) => {
  const token = getToken();
  const response = await instance.put('/api/profile', {
    full_name
  }, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
