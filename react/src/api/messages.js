import instance from './axios';
import { getToken } from '../utils/auth';

export const getMessages = async () => {
  const token = getToken();
  const response = await instance.get('/api/messages', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};

export const sendMessage = async (text) => {
  const token = getToken();
  const response = await instance.post('/api/messages', {
    text
  }, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
