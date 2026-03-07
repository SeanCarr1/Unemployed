
import { describe, it, expect } from 'vitest';
import axios from 'axios';

// Use Vite env variable for API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL;

describe('Registration endpoint', () => {
  it('should return 201 for valid registration', async () => {
    // Use a unique email/username for each run to avoid duplicate errors
    const unique = Date.now();
    const response = await axios.post(`${API_BASE_URL}auth/users/`, {
      email: `testuser${unique}@example.com`,
      username: `testuser${unique}`,
      password: 'pass123456',
      re_password: 'pass123456',
      role: 'seeker',
    });
    expect(response.status).toBe(201);
    expect(response.data).toHaveProperty('id');
    expect(response.data).toHaveProperty('email');
  });
  it('should return 400 for missing fields', async () => {
    try {
      await axios.post(`${API_BASE_URL}auth/users/`, {
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
      await axios.post(`${API_BASE_URL}auth/users/`, {
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
