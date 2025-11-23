import instance from './axios';
import { getToken } from '../utils/auth';

export const register = async (username, full_name, password) => {
  const response = await instance.post('/api/auth/register', {
    username,
    full_name,
    password
  });
  return response.data;
};

export const login = async (username, password) => {
  const response = await instance.post('/api/auth/login', {
    username,
    password
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const token = getToken();
  const response = await instance.get('/api/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
