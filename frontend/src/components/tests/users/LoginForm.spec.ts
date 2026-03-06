import { describe, it, expect } from 'vitest';
import axios from 'axios';

const API_BASE_URL = 'http://backend:8000';

describe('Login endpoint', () => {
  it('should return 400 for missing email', async () => {
    try {
      await axios.post(`${API_BASE_URL}/token/`, {
        email: '',
        password: 'testpass123',
      });
      throw new Error('Should have failed');
    } catch (err: any) {
      expect(err.response.status).toBe(400);
      expect(err.response.data).toBeDefined();
    }
  });

  it('should return 401 for invalid password', async () => {
    try {
      await axios.post(`${API_BASE_URL}/token/`, {
        email: 'testuser@example.com',
        password: 'wrongpass',
      });
      throw new Error('Should have failed');
    } catch (err: any) {
      expect(err.response.status).toBe(401);
      expect(err.response.data).toBeDefined();
    }
  });
});
