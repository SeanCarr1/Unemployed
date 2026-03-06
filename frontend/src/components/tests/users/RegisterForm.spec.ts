import { describe, it, expect } from 'vitest';
import axios from 'axios';

const API_BASE_URL = 'http://backend:8000';

describe('Registration endpoint', () => {
  it('should return 400 for missing fields', async () => {
    try {
      await axios.post(`${API_BASE_URL}/auth/users/`, {
        email: '',
        username: '',
        password: '',
        re_password: '',
        role: null,
      });
      throw new Error('Should have failed');
    } catch (err: any) {
      expect(err.response.status).toBe(400);
      expect(err.response.data).toBeDefined();
    }
  });

  it('should return 400 for password mismatch', async () => {
    try {
      await axios.post(`${API_BASE_URL}/auth/users/`, {
        email: 'test@example.com',
        username: 'testuser',
        password: 'pass123',
        re_password: 'pass456',
        role: 'seeker',
      });
      throw new Error('Should have failed');
    } catch (err: any) {
      expect(err.response.status).toBe(400);
      expect(err.response.data).toBeDefined();
    }
  });
});
