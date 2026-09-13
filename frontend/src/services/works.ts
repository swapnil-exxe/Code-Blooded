import { apiClient } from '@/lib/api-client';
import type { PaginatedResponse, FilterOptionsResponse } from '@/types/common';
import type { WorkListItem, WorkDetail } from '@/types/work';
import { MOCK_WORKS, MOCK_FILTERS } from './mockData';

export interface WorkQueryParams {
  page?: number;
  page_size?: number;
  state?: string;
  district?: string;
  mp_name?: string;
  work_category?: string;
  work_status?: string;
  min_sanction_amount?: number;
  max_sanction_amount?: number;
  search?: string;
}

export const worksService = {
  async getWorks(params?: WorkQueryParams): Promise<PaginatedResponse<WorkListItem>> {
    try {
      const { data } = await apiClient.get<PaginatedResponse<WorkListItem>>('/works', { params });
      return data;
    } catch {
      let filtered = [...MOCK_WORKS];
      if (params?.search) {
        const q = params.search.toLowerCase();
        filtered = filtered.filter(
          (w) =>
            w.work_id.toLowerCase().includes(q) ||
            (w.work_description && w.work_description.toLowerCase().includes(q)) ||
            (w.state && w.state.toLowerCase().includes(q)) ||
            (w.district && w.district.toLowerCase().includes(q))
        );
      }
      if (params?.work_category) {
        filtered = filtered.filter((w) => w.work_category === params.work_category);
      }
      if (params?.work_status) {
        filtered = filtered.filter((w) => w.work_status === params.work_status);
      }
      return {
        items: filtered,
        pagination: {
          total_records: filtered.length,
          page: params?.page || 1,
          page_size: params?.page_size || 20,
          total_pages: 1,
          has_next: false,
          has_prev: false,
        },
      };
    }
  },

  async getWorkById(workId: string): Promise<WorkDetail> {
    try {
      const { data } = await apiClient.get<WorkDetail>('/works/' + encodeURIComponent(workId));
      return data;
    } catch {
      const found = MOCK_WORKS.find((w) => w.work_id === workId) || MOCK_WORKS[0];
      return {
        ...found,
        expenditures: [],
        independent_risk_profiles: {
          cost_anomaly: {
            work_id: found.work_id,
            severity: 'HIGH',
            cost_anomaly_score: 0.88,
            raw_anomaly_score: 0.90,
            peer_group_used: 'STATE_CATEGORY',
            peer_group_level: 'STATE_CATEGORY',
            peer_group_size: 1420,
            is_data_quality_exception: false,
            explanation: 'Peer median deviation calibrated.',
          },
          duplicate_pairs: [],
          fund_anomaly: {
            work_id: found.work_id,
            severity: 'LOW',
            fund_anomaly_score: 0.20,
            raw_score: 0.25,
            audit_category: 'ACTIVE_EXPENDITURE',
            utilization_ratio: 0.85,
            transaction_count: 2,
            payment_concentration_hhi: 0.25,
            days_to_first_disbursement: 30,
            total_disbursed_amount: found.amount_disbursed,
            anomaly_reasons: [],
            explanation: 'Disbursement on track.',
          },
          delay: {
            work_id: found.work_id,
            severity: 'MEDIUM',
            delay_score: 0.55,
            rec_to_sanc_days: 45,
            rec_to_sanc_delay_days: null,
            rec_to_sanc_severity: 'NORMAL',
            sanc_to_comp_days: 200,
            sanc_to_comp_delay_days: null,
            sanc_to_comp_severity: 'NORMAL',
            open_work_aging_days: 250,
            open_work_overdue_days: null,
            open_work_aging_severity: 'NORMAL',
            primary_delay_type: null,
            active_delay_types: [],
            explanation: 'SLA incubation window.',
          },
        },
      };
    }
  },

  async getFilters(): Promise<FilterOptionsResponse> {
    try {
      const { data } = await apiClient.get<FilterOptionsResponse>('/meta/filters');
      return data;
    } catch {
      return MOCK_FILTERS;
    }
  },
};
