import { apiClient } from '@/lib/api-client';
import type { PaginatedResponse } from '@/types/common';
import type { CostAnomalyItem, CostAnomalyDetail } from '@/types/cost_anomaly';
import type { DuplicatePairItem, WorkDuplicateLookupResponse } from '@/types/duplicate_work';
import type { FundAnomalyItem, FundAnomalyDetail } from '@/types/fund_anomaly';
import type { DelayItem, DelayDetail } from '@/types/delay';
import type { DistrictSummaryItem, MPSummaryItem } from '@/types/summaries';
import {
  MOCK_COST_ANOMALIES,
  MOCK_DUPLICATE_WORKS,
  MOCK_FUND_ANOMALIES,
  MOCK_DELAYS,
  MOCK_MP_SUMMARIES,
  MOCK_DISTRICT_SUMMARIES,
} from './mockData';

export const analyticsService = {
  // Model 1: Cost Anomalies
  async getCostAnomalies(params?: {
    severity?: string;
    min_score?: number;
    state?: string;
    district?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<CostAnomalyItem>> {
    try {
      const { data } = await apiClient.get<PaginatedResponse<CostAnomalyItem>>('/analytics/cost-anomalies', { params });
      return data;
    } catch {
      let items = [...MOCK_COST_ANOMALIES];
      if (params?.severity) items = items.filter((i) => i.severity === params.severity);
      return {
        items,
        pagination: {
          total_records: items.length,
          page: params?.page || 1,
          page_size: params?.page_size || 20,
          total_pages: 1,
          has_next: false,
          has_prev: false,
        },
      };
    }
  },

  async getCostAnomalyById(workId: string): Promise<CostAnomalyDetail> {
    try {
      const { data } = await apiClient.get<CostAnomalyDetail>('/analytics/cost-anomalies/' + encodeURIComponent(workId));
      return data;
    } catch {
      const item = MOCK_COST_ANOMALIES.find((i) => i.work_id === workId) || MOCK_COST_ANOMALIES[0];
      return {
        ...item,
        house: 'LOK SABHA',
        work_type: 'Roads & Bridges',
        sanction_amount: 4500000,
        state: 'UTTAR PRADESH',
        district: 'LUCKNOW',
        mp_name: 'RAJNATH SINGH',
      };
    }
  },

  // Model 2: Duplicate Works
  async getDuplicateWorks(params?: {
    severity?: string;
    min_duplicate_score?: number;
    is_same_mp?: boolean;
    is_same_constituency?: boolean;
    state?: string;
    district?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<DuplicatePairItem>> {
    try {
      const { data } = await apiClient.get<PaginatedResponse<DuplicatePairItem>>('/analytics/duplicate-works', { params });
      return data;
    } catch {
      let items = [...MOCK_DUPLICATE_WORKS];
      if (params?.severity) items = items.filter((i) => i.severity === params.severity);
      if (params?.is_same_mp) items = items.filter((i) => i.is_same_mp);
      return {
        items,
        pagination: {
          total_records: items.length,
          page: params?.page || 1,
          page_size: params?.page_size || 20,
          total_pages: 1,
          has_next: false,
          has_prev: false,
        },
      };
    }
  },

  async getDuplicatePairsForWork(workId: string): Promise<WorkDuplicateLookupResponse> {
    try {
      const { data } = await apiClient.get<WorkDuplicateLookupResponse>('/analytics/duplicate-works/pairs/' + encodeURIComponent(workId));
      return data;
    } catch {
      return { work_id: workId, total_flagged_pairs: 1, pairs: MOCK_DUPLICATE_WORKS };
    }
  },

  // Model 3: Fund Anomalies
  async getFundAnomalies(params?: {
    severity?: string;
    audit_category?: string;
    min_score?: number;
    min_utilization?: number;
    max_utilization?: number;
    state?: string;
    district?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<FundAnomalyItem>> {
    try {
      const { data } = await apiClient.get<PaginatedResponse<FundAnomalyItem>>('/analytics/fund-anomalies', { params });
      return data;
    } catch {
      let items = [...MOCK_FUND_ANOMALIES];
      if (params?.severity) items = items.filter((i) => i.severity === params.severity);
      if (params?.audit_category) items = items.filter((i) => i.audit_category === params.audit_category);
      return {
        items,
        pagination: {
          total_records: items.length,
          page: params?.page || 1,
          page_size: params?.page_size || 20,
          total_pages: 1,
          has_next: false,
          has_prev: false,
        },
      };
    }
  },

  async getFundAnomalyById(workId: string): Promise<FundAnomalyDetail> {
    try {
      const { data } = await apiClient.get<FundAnomalyDetail>('/analytics/fund-anomalies/' + encodeURIComponent(workId));
      return data;
    } catch {
      const item = MOCK_FUND_ANOMALIES.find((i) => i.work_id === workId) || MOCK_FUND_ANOMALIES[0];
      return {
        ...item,
        state: 'BIHAR',
        district: 'PATNA',
        sanction_amount: 2800000,
        work_status: 'In Progress',
        mp_name: 'RUDY RAJIV PRATAP',
      };
    }
  },

  // Model 4: Statutory Delays
  async getDelays(params?: {
    severity?: string;
    primary_delay_type?: string;
    min_days_overdue?: number;
    state?: string;
    district?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<DelayItem>> {
    try {
      const { data } = await apiClient.get<PaginatedResponse<DelayItem>>('/analytics/delays', { params });
      return data;
    } catch {
      let items = [...MOCK_DELAYS];
      if (params?.severity) items = items.filter((i) => i.severity === params.severity);
      return {
        items,
        pagination: {
          total_records: items.length,
          page: params?.page || 1,
          page_size: params?.page_size || 20,
          total_pages: 1,
          has_next: false,
          has_prev: false,
        },
      };
    }
  },

  async getDelayById(workId: string): Promise<DelayDetail> {
    try {
      const { data } = await apiClient.get<DelayDetail>('/analytics/delays/' + encodeURIComponent(workId));
      return data;
    } catch {
      const item = MOCK_DELAYS.find((i) => i.work_id === workId) || MOCK_DELAYS[0];
      return {
        ...item,
        state: 'MAHARASHTRA',
        district: 'PUNE',
        mp_name: 'SUPRIYA SULE',
        work_status: 'In Progress',
        sanction_date: '2024-09-01',
        recommended_date: '2024-06-10',
        completion_date: null,
      };
    }
  },

  // Summaries
  async getDistrictSummaries(params?: { state?: string; limit?: number }): Promise<DistrictSummaryItem[]> {
    try {
      const queryParams = { limit: 500, ...params };
      const { data } = await apiClient.get<DistrictSummaryItem[]>('/analytics/district-summary', { params: queryParams });
      return data;
    } catch {
      let items = [...MOCK_DISTRICT_SUMMARIES];
      if (params?.state) items = items.filter((d) => d.state === params.state);
      return items;
    }
  },

  async getMPSummaries(params?: { state?: string; house?: string; limit?: number; mp_name?: string }): Promise<MPSummaryItem[]> {
    try {
      const queryParams = { limit: 500, ...params };
      const { data } = await apiClient.get<MPSummaryItem[]>('/analytics/mp-summary', { params: queryParams });
      return data;
    } catch {
      let items = [...MOCK_MP_SUMMARIES];
      if (params?.house) items = items.filter((m) => m.house === params.house);
      if (params?.mp_name) items = items.filter((m) => m.mp_name.toLowerCase().includes(params.mp_name!.toLowerCase()));
      return items;
    }
  },

  // Trend Analytics Endpoints
  async getNationalTrends(params?: any): Promise<any> {
    try {
      const { data } = await apiClient.get('/analytics/trends/national', { params });
      return data;
    } catch {
      return { total_works: 98825, total_sanctioned: 4500000000, anomaly_rate: 4.8 };
    }
  },

  async getStateTrends(params?: any): Promise<any> {
    try {
      const { data } = await apiClient.get('/analytics/trends/state', { params });
      return data;
    } catch {
      return [];
    }
  },

  async getDistrictTrends(params?: any): Promise<any> {
    try {
      const { data } = await apiClient.get('/analytics/trends/district', { params });
      return data;
    } catch {
      return [];
    }
  },

  async getMPTrends(params?: any): Promise<any> {
    try {
      const { data } = await apiClient.get('/analytics/trends/mp', { params });
      return data;
    } catch {
      return [];
    }
  },

  async getEarlyWarnings(params?: any): Promise<any> {
    try {
      const { data } = await apiClient.get('/analytics/early-warnings', { params });
      return data;
    } catch {
      return [];
    }
  },
};
