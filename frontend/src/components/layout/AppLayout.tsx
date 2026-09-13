import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { RateLimitBanner } from '@/components/common/RateLimitBanner';

export const AppLayout: React.FC = () => {
  return (
    <div className="flex h-screen bg-[#FAF8F5] text-slate-900 overflow-hidden font-sans selection:bg-[#0b192c]/10 selection:text-[#0b192c]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <RateLimitBanner />
        <Header />
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-[#FAF8F5]">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
