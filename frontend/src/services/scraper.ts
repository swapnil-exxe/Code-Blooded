import { apiClient } from '@/lib/api-client';

export interface ScraperLastRun {
  run_id: string;
  start_time: string;
  end_time: string | null;
  status: string;
  records_seen: number;
  records_new: number;
  records_updated: number;
  records_unchanged: number;
  records_invalid: number;
  duration_seconds: number;
  error_message: string | null;
}

export interface ScraperStatusResponse {
  target_url: string;
  interval_hours: number;
  status: string;
  last_run: ScraperLastRun | null;
  total_snapshots_saved: number;
  total_works_in_db: number;
  source_health: string;
}

export const scraperService = {
  async getStatus(): Promise<ScraperStatusResponse> {
    const { data } = await apiClient.get<ScraperStatusResponse>('/admin/scraper/status');
    return data;
  },

  async triggerRun(): Promise<any> {
    const { data } = await apiClient.post('/admin/scraper/run');
    return data;
  },
};
