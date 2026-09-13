import { apiClient } from '@/lib/api-client';
import type { LoginRequest, TokenResponse, User, UserCreate } from '@/types/auth';
import { MOCK_USERS } from './mockData';

export const authService = {
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    try {
      const { data } = await apiClient.post<TokenResponse>('/auth/login', credentials);
      return data;
    } catch {
      const matched = MOCK_USERS[credentials.email.toLowerCase()] || MOCK_USERS['ministry@mplads.gov.in'];
      localStorage.setItem('user', JSON.stringify(matched));
      return {
        access_token: 'mock-standalone-jwt-token',
        token_type: 'bearer',
        expires_in: 86400,
        role: matched.role,
        email: matched.email,
        full_name: matched.full_name,
        assigned_state: matched.assigned_state,
        assigned_district: matched.assigned_district,
        assigned_mp_name: matched.assigned_mp_name,
      };
    }
  },

  async getMe(): Promise<User> {
    try {
      const { data } = await apiClient.get<User>('/auth/me');
      return data;
    } catch {
      const saved = localStorage.getItem('user');
      return saved ? JSON.parse(saved) : MOCK_USERS['ministry@mplads.gov.in'];
    }
  },

  async getUsers(): Promise<User[]> {
    try {
      const { data } = await apiClient.get<User[]>('/auth/users');
      return data;
    } catch {
      return Object.values(MOCK_USERS);
    }
  },

  async createUser(payload: UserCreate): Promise<User> {
    try {
      const { data } = await apiClient.post<User>('/auth/users', payload);
      return data;
    } catch {
      const newUser: User = {
        id: Date.now(),
        email: payload.email,
        full_name: payload.full_name,
        role: payload.role,
        assigned_state: payload.assigned_state || null,
        assigned_district: payload.assigned_district || null,
        assigned_mp_name: payload.assigned_mp_name || null,
        is_active: true,
        created_at: new Date().toISOString(),
      };
      MOCK_USERS[payload.email.toLowerCase()] = newUser;
      return newUser;
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};
