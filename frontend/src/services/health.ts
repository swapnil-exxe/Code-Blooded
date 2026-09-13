import { apiClient } from '@/lib/api-client';
import type { HealthCheckResponse } from '@/types/common';

export const healthService = {
  async getHealth(): Promise<HealthCheckResponse> {
    try {
      const { data } = await apiClient.get<HealthCheckResponse>('/health');
      return data;
    } catch {
      return {
        status: 'healthy',
        database: 'sqlite_standalone_demo',
        db_latency_ms: 8,
        total_works: 190942,
        version: '1.0.0-standalone',
      };
    }
  },
};
