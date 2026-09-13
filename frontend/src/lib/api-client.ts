import axios from 'axios';

export function getApiBaseUrl(): string {
  let envUrl = (import.meta.env.VITE_API_BASE_URL || '/api/v1').trim();
  if (envUrl.endsWith('/')) {
    envUrl = envUrl.slice(0, -1);
  }
  if (!envUrl.includes('/api/v1')) {
    if (envUrl.endsWith('/api')) {
      envUrl = `${envUrl}/v1`;
    } else {
      envUrl = `${envUrl}/api/v1`;
    }
  }
  return envUrl;
}

const baseURL = getApiBaseUrl();

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT Bearer token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = 'Bearer ' + token;
  }
  return config;
});

// Custom event for rate limiting notifications
export const RATE_LIMIT_EVENT = 'rate_limit_exceeded';

export interface RateLimitDetail {
  retryAfter: number;
}

// Response interceptor for 401 and 429
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      } else if (error.response.status === 429) {
        // SlowAPI rate limit exceeded
        const retryAfterHeader = error.response.headers['retry-after'];
        const retryAfter = retryAfterHeader ? parseInt(retryAfterHeader, 10) : 60;
        window.dispatchEvent(
          new CustomEvent<RateLimitDetail>(RATE_LIMIT_EVENT, {
            detail: { retryAfter: isNaN(retryAfter) ? 60 : retryAfter },
          })
        );
      }
    }
    return Promise.reject(error);
  }
);
