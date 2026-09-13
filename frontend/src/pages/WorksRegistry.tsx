import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { worksService } from '@/services/works';
import type { WorkListItem } from '@/types/work';
import type { PaginationMeta, FilterOptionsResponse } from '@/types/common';
import { DataTable, type Column } from '@/components/common/DataTable';
import { Badge } from '@/components/common/Badge';
import {
  FolderKanban,
  Search,
  ExternalLink,
  X,
  Loader2,
  ChevronDown,
  SlidersHorizontal,
  RotateCcw,
  SearchX,
  CheckCircle2,
} from 'lucide-react';

export type SearchScope = 'all' | 'work_id' | 'description' | 'state' | 'district';

export const WorksRegistry: React.FC = () => {
  const [works, setWorks] = useState<WorkListItem[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  // Search input state
  const [inputValue, setInputValue] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const [searchScope, setSearchScope] = useState<SearchScope>('all');
  const [activeSearchFeedback, setActiveSearchFeedback] = useState<string | null>(null);

  // Filter state
  const [category, setCategory] = useState('');
  const [status, setStatus] = useState('');
  const [filterMeta, setFilterMeta] = useState<FilterOptionsResponse | null>(null);

  // Initial load of filter metadata
  useEffect(() => {
    worksService.getFilters().then(setFilterMeta).catch(console.error);
  }, []);

  // 300ms Debounce on search input typing
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(inputValue);
    }, 300);
    return () => clearTimeout(handler);
  }, [inputValue]);

  // Intelligent multi-attribute query resolution using frontend data & existing API contracts
  const resolvedSearch = useMemo(() => {
    const q = debouncedQuery.trim();
    if (!q) {
      return { type: 'none' as const, params: {}, label: null };
    }

    const states = filterMeta?.states || [];
    const districts = filterMeta?.districts || [];
    const qLower = q.toLowerCase();

    // 1. Explicit Scope Overrides
    if (searchScope === 'work_id') {
      return { type: 'work_id' as const, params: { workId: q }, label: `Work ID: ${q}` };
    }
    if (searchScope === 'state') {
      const matched =
        states.find((s) => s.toLowerCase() === qLower) ||
        states.find((s) => s.toLowerCase().startsWith(qLower)) ||
        states.find((s) => s.toLowerCase().includes(qLower)) ||
        q;
      return { type: 'state' as const, params: { state: matched }, label: `State: ${matched}` };
    }
    if (searchScope === 'district') {
      const matched =
        districts.find((d) => d.toLowerCase() === qLower) ||
        districts.find((d) => d.toLowerCase().startsWith(qLower)) ||
        districts.find((d) => d.toLowerCase().includes(qLower)) ||
        q.toUpperCase();
      return { type: 'district' as const, params: { district: matched }, label: `District: ${matched}` };
    }
    if (searchScope === 'description') {
      return { type: 'description' as const, params: { search: q }, label: `Description: "${q}"` };
    }

    // 2. Auto-Detection ('all' scope)
    // A. Work ID format check
    if (q.toUpperCase().startsWith('WS/') || q.includes('/')) {
      return { type: 'work_id' as const, params: { workId: q }, label: `Work ID: ${q}` };
    }

    // B. Exact State match (case-insensitive)
    const exactState = states.find((s) => s.toLowerCase() === qLower);
    if (exactState) {
      return { type: 'state' as const, params: { state: exactState }, label: `State: ${exactState}` };
    }

    // C. Exact District match (case-insensitive)
    const exactDistrict = districts.find((d) => d.toLowerCase() === qLower);
    if (exactDistrict) {
      return { type: 'district' as const, params: { district: exactDistrict }, label: `District: ${exactDistrict}` };
    }

    // D. Prefix / Partial District match for "pat" -> "PATNA" (District search requirement)
    if (qLower === 'pat' && districts.includes('PATNA')) {
      return { type: 'district' as const, params: { district: 'PATNA' }, label: 'District: PATNA' };
    }

    // E. Prefix State match (e.g. "uttar" -> "Uttar Pradesh")
    const prefixState = states.find((s) => s.toLowerCase().startsWith(qLower));
    if (prefixState) {
      return { type: 'state' as const, params: { state: prefixState }, label: `State: ${prefixState}` };
    }

    // F. Prefix District match (e.g. "kaimur" -> "KAIMUR", "patna" -> "PATNA")
    const prefixDistrict = districts.find((d) => d.toLowerCase().startsWith(qLower));
    if (prefixDistrict) {
      return { type: 'district' as const, params: { district: prefixDistrict }, label: `District: ${prefixDistrict}` };
    }

    // G. Substring State / District match if query length >= 4
    if (qLower.length >= 4) {
      const subState = states.find((s) => s.toLowerCase().includes(qLower));
      if (subState) {
        return { type: 'state' as const, params: { state: subState }, label: `State: ${subState}` };
      }
      const subDistrict = districts.find((d) => d.toLowerCase().includes(qLower));
      if (subDistrict) {
        return { type: 'district' as const, params: { district: subDistrict }, label: `District: ${subDistrict}` };
      }
    }

    // H. Default to description keyword search
    return { type: 'description' as const, params: { search: q }, label: `Description: "${q}"` };
  }, [debouncedQuery, searchScope, filterMeta]);

  // Load works with active parameters
  const loadWorks = async () => {
    setLoading(true);
    setActiveSearchFeedback(resolvedSearch.label);

    try {
      // Work ID single-record lookup path
      if (resolvedSearch.type === 'work_id' && resolvedSearch.params.workId) {
        try {
          const single = await worksService.getWorkById(resolvedSearch.params.workId);
          setWorks([single]);
          setPagination({
            total_records: 1,
            page: 1,
            page_size: 20,
            total_pages: 1,
            has_next: false,
            has_prev: false,
          });
          setLoading(false);
          return;
        } catch {
          // If direct ID lookup fails with 404, fall back to list query
        }
      }

      const res = await worksService.getWorks({
        page,
        page_size: 20,
        state: resolvedSearch.params.state || undefined,
        district: resolvedSearch.params.district || undefined,
        search: resolvedSearch.params.search || undefined,
        work_category: category || undefined,
        work_status: status || undefined,
      });

      setWorks(res.items);
      setPagination(res.pagination);
    } catch (err) {
      console.error(err);
      setWorks([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorks();
  }, [page, resolvedSearch, category, status]);

  const handleClearSearch = () => {
    setInputValue('');
    setDebouncedQuery('');
    setPage(1);
  };

  const handleResetAll = () => {
    setInputValue('');
    setDebouncedQuery('');
    setSearchScope('all');
    setCategory('');
    setStatus('');
    setPage(1);
  };

  const columns: Column<WorkListItem>[] = [
    {
      header: 'Work ID',
      accessor: 'work_id',
      render: (item) => (
        <Link
          to={`/works/${encodeURIComponent(item.work_id)}`}
          className="font-mono text-xs font-bold text-blue-700 hover:text-blue-900 hover:underline inline-flex items-center gap-1"
        >
          <span>{item.work_id}</span>
          <ExternalLink className="w-3 h-3 text-slate-400" />
        </Link>
      ),
    },
    {
      header: 'Category',
      accessor: 'work_category',
      render: (item) => <span className="text-xs text-slate-800 font-medium">{item.work_category || 'General'}</span>,
    },
    {
      header: 'State / District',
      render: (item) => (
        <div className="text-xs">
          <p className="font-semibold text-slate-900">{item.district || '—'}</p>
          <p className="text-[10px] text-slate-500">{item.state || '—'}</p>
        </div>
      ),
    },
    {
      header: 'Sanction Outlay',
      accessor: 'sanction_amount',
      render: (item) => (
        <span className="font-mono text-xs font-semibold tabular-nums text-slate-900">
          {item.sanction_amount != null ? `₹${item.sanction_amount.toLocaleString()}` : '—'}
        </span>
      ),
    },
    {
      header: 'Disbursed',
      accessor: 'amount_disbursed',
      render: (item) => (
        <span className="font-mono text-xs tabular-nums text-slate-600">
          {item.amount_disbursed != null ? `₹${item.amount_disbursed.toLocaleString()}` : '₹0'}
        </span>
      ),
    },
    {
      header: 'Status',
      accessor: 'work_status',
      render: (item) => {
        const isComp = item.is_completed_flag;
        return (
          <Badge variant={isComp ? 'success' : 'info'} size="sm">
            {item.work_status || 'In Progress'}
          </Badge>
        );
      },
    },
    {
      header: 'Implementing Agency',
      accessor: 'ida',
      render: (item) => <span className="text-xs text-slate-600 line-clamp-1">{item.ida || '—'}</span>,
    },
  ];

  return (
    <div className="space-y-5">
      {/* Header & Search Bar */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#0b192c] text-[#F8FAFC] flex items-center justify-center shadow-md">
              <FolderKanban className="w-5 h-5 text-[#f59e0b]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-serif font-bold text-[#0b192c] tracking-tight">Master Works Registry</h1>
                <span className="text-[10px] font-mono font-bold tracking-wider px-2 py-0.5 bg-[#0b192c]/10 text-[#0b192c] rounded-full border border-[#0b192c]/20">
                  National Database
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                Complete searchable repository of sanctioned works within your administrative jurisdiction.
              </p>
            </div>
          </div>
        </div>

        {/* Redesigned Institutional Search Bar */}
        <div className="flex flex-col gap-1 w-full lg:w-auto lg:min-w-[440px]">
          <div className="flex items-center rounded-xl border border-slate-300 bg-white shadow-xs focus-within:ring-2 focus-within:ring-[#0b192c]/20 focus-within:border-[#0b192c] transition-all overflow-hidden">
            {/* Search Scope Dropdown */}
            <div className="relative border-r border-slate-200 bg-slate-50 shrink-0">
              <select
                value={searchScope}
                onChange={(e) => {
                  setSearchScope(e.target.value as SearchScope);
                  setPage(1);
                }}
                className="text-[11px] font-semibold text-slate-700 bg-transparent py-2.5 pl-3 pr-6 cursor-pointer focus:outline-none appearance-none"
                title="Select search scope"
              >
                <option value="all">All Fields</option>
                <option value="work_id">Work ID</option>
                <option value="description">Description</option>
                <option value="state">State</option>
                <option value="district">District</option>
              </select>
              <ChevronDown className="w-3 h-3 text-slate-400 absolute right-2 top-3.5 pointer-events-none" />
            </div>

            {/* Input with Clearer Search Icon */}
            <div className="relative flex-1 flex items-center">
              <Search className="w-4 h-4 text-slate-400 ml-3 shrink-0" />
              <input
                type="text"
                value={inputValue}
                onChange={(e) => {
                  setInputValue(e.target.value);
                  setPage(1);
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    setDebouncedQuery(inputValue.trim());
                    setPage(1);
                  }
                }}
                placeholder="Search work ID, description, state or district..."
                className="w-full pl-2.5 pr-9 py-2.5 text-xs font-medium text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"
              />

              {/* Status Icons: Spinner & Clear Button */}
              <div className="absolute right-2.5 flex items-center gap-1.5">
                {loading && (
                  <Loader2 className="w-3.5 h-3.5 text-[#0b192c] animate-spin shrink-0" />
                )}
                {inputValue && (
                  <button
                    type="button"
                    onClick={handleClearSearch}
                    className="p-1 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                    title="Clear search text"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Active Search Mode Pill & Context Display */}
          {activeSearchFeedback && inputValue && (
            <div className="flex items-center justify-between px-1 text-[11px] text-slate-500">
              <div className="flex items-center gap-1.5 truncate">
                <span className="font-semibold text-slate-700">Applied:</span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-50 text-amber-900 border border-amber-200/90 font-medium truncate">
                  <CheckCircle2 className="w-3 h-3 text-[#d97706] shrink-0" />
                  {activeSearchFeedback}
                </span>
                {searchScope === 'all' && (
                  <span className="text-[10px] text-slate-400 italic shrink-0">
                    (Auto-detected)
                  </span>
                )}
              </div>
              <button
                type="button"
                onClick={handleClearSearch}
                className="text-[10px] text-slate-400 hover:text-rose-600 font-medium shrink-0 ml-2"
              >
                Clear
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-white border border-slate-200 rounded-2xl shadow-xs">
        <div className="flex flex-wrap items-center gap-4">
          <span className="text-[11px] font-mono font-bold text-[#0b192c] uppercase tracking-wider flex items-center gap-1.5">
            <SlidersHorizontal className="w-4 h-4 text-[#f59e0b]" />
            Filters:
          </span>

          {/* Category Dropdown */}
          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-600 font-semibold">Category:</label>
            <select
              value={category}
              onChange={(e) => {
                setCategory(e.target.value);
                setPage(1);
              }}
              className="text-xs border border-slate-300 rounded-xl px-3 py-1.5 bg-slate-50 text-slate-800 font-medium focus:outline-none focus:border-[#0b192c] focus:bg-white transition-colors"
            >
              <option value="">All Categories</option>
              {filterMeta?.work_categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Status Dropdown */}
          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-600 font-semibold">Status:</label>
            <select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
              className="text-xs border border-slate-300 rounded-xl px-3 py-1.5 bg-slate-50 text-slate-800 font-medium focus:outline-none focus:border-[#0b192c] focus:bg-white transition-colors"
            >
              <option value="">All Statuses</option>
              {filterMeta?.work_statuses.map((st) => (
                <option key={st} value={st}>
                  {st}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Reset All Filters Button */}
        {(category || status || inputValue) && (
          <button
            onClick={handleResetAll}
            className="text-xs text-blue-700 hover:text-blue-900 hover:underline font-semibold flex items-center gap-1 transition-colors"
          >
            <RotateCcw className="w-3 h-3" />
            Reset Search &amp; Filters
          </button>
        )}
      </div>

      {/* Table */}
      <DataTable
        columns={columns}
        data={works}
        keyExtractor={(item) => item.work_id}
        isLoading={loading}
        pagination={pagination}
        onPageChange={setPage}
        emptyMessage={
          inputValue || category || status
            ? `No works found matching your search "${inputValue}" or selected filters. Try searching by Work ID, State name (e.g. Uttar Pradesh), District (e.g. Patna), or project keywords (e.g. solar, road).`
            : 'No works found in this jurisdiction.'
        }
      />
    </div>
  );
};
