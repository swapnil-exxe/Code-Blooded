import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { analyticsService } from '@/services/analytics';
import type { FundAnomalyItem } from '@/types/fund_anomaly';
import type { PaginationMeta } from '@/types/common';
import { DataTable, type Column } from '@/components/common/DataTable';
import { SeverityBadge, Badge } from '@/components/common/Badge';
import { BadgePercent, Filter, ExternalLink } from 'lucide-react';

export const FundAnomalies: React.FC = () => {
  const [items, setItems] = useState<FundAnomalyItem[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [severity, setSeverity] = useState<string>('');
  const [category, setCategory] = useState<string>('');

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await analyticsService.getFundAnomalies({
        page,
        page_size: 20,
        severity: severity || undefined,
        audit_category: category || undefined,
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
  }, [page, severity, category]);

  const columns: Column<FundAnomalyItem>[] = [
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
      header: 'Audit Category',
      accessor: 'audit_category',
      render: (item) => (
        <Badge variant="neutral" size="sm">
          {item.audit_category.replace(/_/g, ' ')}
        </Badge>
      ),
    },
    {
      header: 'Disbursed Amount',
      accessor: 'total_disbursed_amount',
      render: (item) => (
        <span className="font-mono text-xs font-semibold text-slate-800">
          {item.total_disbursed_amount != null ? `₹${item.total_disbursed_amount.toLocaleString()}` : '₹0'}
        </span>
      ),
    },
    {
      header: 'Utilization',
      accessor: 'utilization_ratio',
      render: (item) => (
        <span className="font-mono text-xs text-slate-700">
          {item.utilization_ratio != null ? `${(item.utilization_ratio * 100).toFixed(1)}%` : '—'}
        </span>
      ),
    },
    {
      header: 'Vendor HHI',
      accessor: 'payment_concentration_hhi',
      render: (item) => (
        <span className="font-mono text-xs text-slate-700" title="Herfindahl-Hirschman Index">
          {item.payment_concentration_hhi != null ? item.payment_concentration_hhi.toFixed(3) : '—'}
        </span>
      ),
    },
    {
      header: 'Score',
      accessor: 'fund_anomaly_score',
      render: (item) => (
        <span className="font-mono text-xs font-bold text-slate-800">
          {(item.fund_anomaly_score * 100).toFixed(1)}%
        </span>
      ),
    },
    {
      header: 'Audit Explanation',
      accessor: 'explanation',
      className: 'max-w-xs',
      render: (item) => (
        <p className="text-xs text-slate-600 line-clamp-2" title={item.explanation || ''}>
          {item.explanation || 'Financial pattern verified against normal ledger flow.'}
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
              <BadgePercent className="w-5 h-5 text-[#f59e0b]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-serif font-bold text-[#0b192c] tracking-tight">
                  Model 3 — Fund & Expenditure Anomaly
                </h1>
                <span className="text-[10px] font-mono font-bold tracking-wider px-2 py-0.5 bg-amber-50 text-amber-900 rounded-full border border-amber-200">
                  Financial Reconciliation
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                Financial reconciliation, vendor payment concentration (HHI), and disbursement dormancy.
              </p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-2 bg-white p-2 border border-slate-200 rounded-xl shadow-xs">
          <Filter className="w-4 h-4 text-[#f59e0b] ml-1" />
          <select
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setPage(1);
            }}
            className="text-xs border border-slate-300 rounded-lg px-3 py-1.5 bg-slate-50 text-slate-800 font-semibold focus:outline-none focus:border-[#0b192c] focus:bg-white transition-colors"
          >
            <option value="">All Categories</option>
            <option value="ACTIVE_EXPENDITURE">Active Expenditure</option>
            <option value="NORMAL_AWAITING_DISBURSEMENT">Awaiting Disbursement</option>
            <option value="DORMANT_SANCTION">Dormant Sanction</option>
            <option value="STATUS_EXPENDITURE_MISMATCH">Status Mismatch</option>
          </select>

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
        emptyMessage="No fund & expenditure anomalies found matching criteria."
      />
    </div>
  );
};
