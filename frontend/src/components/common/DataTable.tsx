import React from 'react';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight, Inbox } from 'lucide-react';
import type { PaginationMeta } from '@/types/common';

export interface Column<T> {
  header: string | React.ReactNode;
  accessor?: keyof T;
  render?: (item: T) => React.ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string | number;
  isLoading?: boolean;
  pagination?: PaginationMeta;
  onPageChange?: (page: number) => void;
  emptyMessage?: string;
}

export function DataTable<T>({
  columns,
  data,
  keyExtractor,
  isLoading = false,
  pagination,
  onPageChange,
  emptyMessage = 'No records found matching criteria.',
}: DataTableProps<T>) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-100/80 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-[#0b192c]">
              {columns.map((col, idx) => (
                <th key={idx} className={`py-3 px-4 ${col.className || ''}`}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading ? (
              Array.from({ length: 6 }).map((_, rIdx) => (
                <tr key={rIdx} className="animate-pulse">
                  {columns.map((_, cIdx) => (
                    <td key={cIdx} className="py-3 px-4">
                      <div className="h-3.5 bg-slate-200/70 rounded-md w-3/4"></div>
                    </td>
                  ))}
                </tr>
              ))
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="py-12 text-center text-slate-400">
                  <Inbox className="w-9 h-9 mx-auto mb-2 text-slate-300" />
                  <p className="text-xs font-medium text-slate-500">{emptyMessage}</p>
                </td>
              </tr>
            ) : (
              data.map((item) => (
                <tr key={keyExtractor(item)} className="hover:bg-amber-50/30 transition-colors">
                  {columns.map((col, cIdx) => (
                    <td key={cIdx} className={`py-3 px-4 text-slate-700 ${col.className || ''}`}>
                      {col.render ? col.render(item) : col.accessor ? String(item[col.accessor] ?? '—') : '—'}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {pagination && (
        <div className="py-3 px-4 border-t border-slate-200 bg-[#FAF8F5]/80 flex items-center justify-between text-xs text-slate-600">
          <div className="tabular-nums font-medium">
            Showing Page <strong className="text-[#0b192c]">{pagination.page}</strong> of{' '}
            <strong className="text-[#0b192c]">{pagination.total_pages}</strong> ({' '}
            <strong className="text-[#0b192c]">{pagination.total_records.toLocaleString()}</strong> total records)
          </div>
          <div className="flex items-center gap-1.5">
            <button
              onClick={() => onPageChange?.(1)}
              disabled={pagination.page <= 1 || isLoading}
              className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-xs"
              title="First Page"
            >
              <ChevronsLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => onPageChange?.(pagination.page - 1)}
              disabled={!pagination.has_prev || isLoading}
              className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-xs"
              title="Previous Page"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-2.5 font-bold tabular-nums text-xs text-[#0b192c]">
              {pagination.page} / {pagination.total_pages}
            </span>
            <button
              onClick={() => onPageChange?.(pagination.page + 1)}
              disabled={!pagination.has_next || isLoading}
              className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-xs"
              title="Next Page"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onPageChange?.(pagination.total_pages)}
              disabled={pagination.page >= pagination.total_pages || isLoading}
              className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-xs"
              title="Last Page"
            >
              <ChevronsRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
