import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { analyticsService } from '@/services/analytics';
import type { CostAnomalyItem } from '@/types/cost_anomaly';
import type { PaginationMeta } from '@/types/common';
import { DataTable, type Column } from '@/components/common/DataTable';
import { SeverityBadge } from '@/components/common/Badge';
import { AlertTriangle, Filter, ExternalLink } from 'lucide-react';

export const CostAnomalies: React.FC = () => {
  const [items, setItems] = useState<CostAnomalyItem[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [severity, setSeverity] = useState<string>('');

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await analyticsService.getCostAnomalies({
        page,
        page_size: 20,
        severity: severity || undefined,
      });
      setItems(res.items);
      setPagination(res.pagination);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, severity]);

  const columns: Column<CostAnomalyItem>[] = [
    {
      header: 'Work ID',
      accessor: 'work_id',
      render: (item) => (
        <Link
          to={`/works/${encodeURIComponent(item.work_id)}`}
          className="font-mono text-xs font-semibold text-blue-600 hover:underline flex items-center gap-1"
        >
          <span>{item.work_id}</span>
          <ExternalLink className="w-3 h-3" />
        </Link>
      ),
    },
    {
      header: 'Severity',
      accessor: 'severity',
      render: (item) => <SeverityBadge severity={item.severity} />,
    },
    {
      header: 'Calibrated Score',
      accessor: 'cost_anomaly_score',
      render: (item) => (
        <span className="font-mono text-xs font-bold text-slate-800">
          {(item.cost_anomaly_score * 100).toFixed(1)}%
        </span>
      ),
    },
    {
      header: 'Peer Group Used',
      accessor: 'peer_group_used',
      render: (item) => (
        <span className="text-xs text-slate-600">
          {item.peer_group_used || 'General Peer Group'} ({item.peer_group_level || 'L1'})
        </span>
      ),
    },
    {
      header: 'Peer Sample Size',
      accessor: 'peer_group_size',
      render: (item) => (
        <span className="text-xs text-slate-600 font-mono">
          {item.peer_group_size ? item.peer_group_size.toLocaleString() : '—'}
        </span>
      ),
    },
    {
      header: 'Statutory Explanation',
      accessor: 'explanation',
      className: 'max-w-md',
      render: (item) => (
        <p className="text-xs text-slate-600 line-clamp-2" title={item.explanation || ''}>
          {item.explanation || 'Evaluated against category peer median.'}
        </p>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#0b192c] text-[#F8FAFC] flex items-center justify-center shadow-md">
              <AlertTriangle className="w-5 h-5 text-[#f59e0b]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-serif font-bold text-[#0b192c] tracking-tight">
                  Model 1 — Cost Anomaly Detection
                </h1>
                <span className="text-[10px] font-mono font-bold tracking-wider px-2 py-0.5 bg-rose-50 text-rose-800 rounded-full border border-rose-200">
                  Isolation Forest
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                Hierarchical Isolation Forest & peer median deviation calibrated by work category.
              </p>
            </div>
          </div>
        </div>

        {/* Filter */}
        <div className="flex items-center gap-2 bg-white p-2 border border-slate-200 rounded-xl shadow-xs">
          <Filter className="w-4 h-4 text-[#f59e0b] ml-1" />
          <select
            value={severity}
            onChange={(e) => {
              setSeverity(e.target.value);
              setPage(1);
            }}
            className="text-xs border border-slate-300 rounded-lg px-3 py-1.5 bg-slate-50 text-slate-800 font-semibold focus:outline-none focus:border-[#0b192c] focus:bg-white transition-colors"
          >
            <option value="">All Severities</option>
            <option value="HIGH">HIGH (Requires Review)</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <DataTable
        columns={columns}
        data={items}
        keyExtractor={(item) => item.work_id}
        isLoading={loading}
        pagination={pagination}
        onPageChange={setPage}
        emptyMessage="No cost anomalies found matching the selected criteria."
      />
    </div>
  );
};
