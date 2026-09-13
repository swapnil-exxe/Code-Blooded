import React from 'react';
import type { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  badge?: string;
  variant?: 'default' | 'alert' | 'warning' | 'success';
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badge,
  variant = 'default',
  className = '',
}) => {
  const borderStyles = {
    default: 'border-slate-200 hover:border-slate-300 bg-white',
    alert: 'border-rose-200 bg-white hover:border-rose-300',
    warning: 'border-amber-200 bg-white hover:border-amber-300',
    success: 'border-emerald-200 bg-white hover:border-emerald-300',
  };

  const iconColors = {
    default: 'text-slate-700 bg-slate-100 border-slate-200',
    alert: 'text-rose-700 bg-rose-50 border-rose-200',
    warning: 'text-amber-700 bg-amber-50 border-amber-200',
    success: 'text-emerald-700 bg-emerald-50 border-emerald-200',
  };

  return (
    <div className={`p-5 bg-white rounded-2xl border shadow-xs transition-all ${borderStyles[variant]} ${className}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <p className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-500 truncate">{title}</p>
          <p className="mt-2 text-2xl sm:text-3xl font-extrabold text-[#0b192c] tabular-nums tracking-tight">{value}</p>
        </div>
        {Icon && (
          <div className={`p-2.5 rounded-xl border shrink-0 ${iconColors[variant]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      {(subtitle || badge) && (
        <div className="mt-3 flex items-center justify-between gap-2 border-t border-slate-100 pt-2.5">
          {subtitle && <p className="text-xs text-slate-500 truncate">{subtitle}</p>}
          {badge && (
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full border border-slate-200 bg-slate-50 text-slate-700 shrink-0">
              {badge}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
