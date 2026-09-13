import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import {
  LayoutDashboard,
  FolderKanban,
  AlertTriangle,
  Copy,
  BadgePercent,
  Clock,
  MapPin,
  Users,
  UserCog,
  ShieldCheck,
  Building2,
  TrendingUp,
  Globe,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs transition-all ${
      isActive
        ? 'bg-[#132238] text-white font-semibold border-l-2 border-amber-400 shadow-xs'
        : 'text-slate-300 hover:bg-slate-800/60 hover:text-white font-medium'
    }`;

  const moduleNavClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-all ${
      isActive
        ? 'bg-[#132238] text-white font-semibold border-l-2 border-amber-400 shadow-xs'
        : 'text-slate-300 hover:bg-slate-800/60 hover:text-white font-medium'
    }`;

  return (
    <aside className="w-64 bg-[#0B1528] text-slate-200 flex flex-col shrink-0 h-screen sticky top-0 border-r border-slate-800/80 select-none">
      {/* Brand Header */}
      <div className="h-16 px-4 flex items-center gap-3 border-b border-slate-800/80 bg-[#0A1325]">
        <div className="w-9 h-9 rounded-full bg-white flex items-center justify-center shrink-0 p-0.5 border border-amber-400/50 shadow-md">
          <img src="/mplads-logo.png" alt="MPLADS Official Logo" className="w-full h-full object-contain rounded-full" />
        </div>
        <div className="min-w-0">
          <div className="flex items-center gap-1.5">
            <h1 className="font-bold text-sm tracking-tight text-white leading-none">GOVERNANCE</h1>
            <span className="text-[9px] font-mono font-bold tracking-wider px-1.5 py-0.5 bg-blue-600/30 text-blue-300 rounded border border-blue-400/30">
              AI MONITOR
            </span>
          </div>
          <p className="text-[10px] text-slate-400 font-medium mt-1 truncate">AI Analytics & Monitoring Platform</p>
        </div>
      </div>

      {/* Navigation Sections */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
        {/* Section 1: Monitoring */}
        <div>
          <div className="px-3 pb-2 text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">
            MONITORING
          </div>
          <div className="space-y-0.5">
            <NavLink to="/dashboard" className={navClass}>
              <LayoutDashboard className="w-4 h-4 text-slate-400" />
              <span>Executive Dashboard</span>
            </NavLink>
            <NavLink to="/works" className={navClass}>
              <FolderKanban className="w-4 h-4 text-slate-400" />
              <span>Works Master Registry</span>
            </NavLink>
          </div>
        </div>

        {/* Section 2: Analytical Modules (Always Visible) */}
        <div>
          <div className="px-3 pb-2 text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">
            ANALYTICAL MODULES
          </div>
          <div className="space-y-0.5">
            <NavLink to="/analytics/cost-anomalies" className={moduleNavClass}>
              <div className="flex items-center gap-2.5">
                <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                <span>Cost Anomaly Detection</span>
              </div>
              <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
            </NavLink>
            <NavLink to="/analytics/duplicate-works" className={moduleNavClass}>
              <div className="flex items-center gap-2.5">
                <Copy className="w-3.5 h-3.5 text-indigo-400" />
                <span>Duplicate Work Detection</span>
              </div>
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
            </NavLink>
            <NavLink to="/analytics/fund-anomalies" className={moduleNavClass}>
              <div className="flex items-center gap-2.5">
                <BadgePercent className="w-3.5 h-3.5 text-amber-400" />
                <span>Fund & Expenditure Audit</span>
              </div>
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            </NavLink>
            <NavLink to="/analytics/delays" className={moduleNavClass}>
              <div className="flex items-center gap-2.5">
                <Clock className="w-3.5 h-3.5 text-blue-400" />
                <span>Statutory Delay Tracking</span>
              </div>
              <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
            </NavLink>
            <NavLink to="/analytics/trends" className={moduleNavClass}>
              <div className="flex items-center gap-2.5">
                <TrendingUp className="w-3.5 h-3.5 text-purple-400" />
                <span>Trend & Aggregate Analytics</span>
              </div>
              <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
            </NavLink>
          </div>
        </div>

        {/* Section 3: Governance */}
        <div>
          <div className="px-3 pb-2 text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">
            GOVERNANCE
          </div>
          <div className="space-y-0.5">
            <NavLink to="/analytics/district-summary" className={navClass}>
              <MapPin className="w-4 h-4 text-slate-400" />
              <span>District Performance</span>
            </NavLink>
            <NavLink to="/analytics/mp-summary" className={navClass}>
              <Users className="w-4 h-4 text-slate-400" />
              <span>MP Portfolio Summary</span>
            </NavLink>
          </div>
        </div>

        {/* Section 4: Administration Console (Ministry Only) */}
        {user?.role === 'MINISTRY' && (
          <div>
            <div className="px-3 pb-2 text-[10px] font-mono font-bold uppercase tracking-widest text-slate-400">
              ADMINISTRATION
            </div>
            <div className="space-y-0.5">
              <NavLink to="/admin/users" className={navClass}>
                <UserCog className="w-4 h-4 text-emerald-400" />
                <span>Stakeholder Accounts</span>
              </NavLink>
              <NavLink to="/admin/source-monitor" className={navClass}>
                <Globe className="w-4 h-4 text-amber-400" />
                <span>Data Source Monitor</span>
              </NavLink>
            </div>
          </div>
        )}
      </div>

      {/* Footer Lineage & Team Attribution */}
      <div className="p-3.5 border-t border-slate-800/80 bg-[#0A1325] text-[10px] text-slate-400">
        <div className="flex items-center gap-1.5 font-medium text-slate-300">
          <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
          <span>MoSPI Governance Platform</span>
        </div>
        <p className="mt-1 text-[9px] text-slate-500 leading-tight">
          Zero Composite Risk • 4 Isolated Models • PostgreSQL RLS Enforced
        </p>
      </div>
    </aside>
  );
};
