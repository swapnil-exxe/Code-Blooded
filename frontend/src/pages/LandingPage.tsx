import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { 
  Building2, 
  ArrowRight, 
  ShieldCheck, 
  Layers, 
  TrendingUp, 
  Copy, 
  Clock, 
  Landmark, 
  Sparkles, 
  ChevronRight, 
  Menu, 
  X,
  FileSearch,
  LayoutDashboard,
  LogOut,
  Globe,
  RefreshCw,
  Database,
  CheckCircle2,
  Zap,
  HelpCircle,
  Lock,
  Shield,
  ChevronDown,
  ChevronUp,
  BarChart3
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [videoError, setVideoError] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  const scrollToSection = (id: string) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF8F5]/80 text-slate-900 font-sans selection:bg-[#0b192c]/10 selection:text-[#0b192c] flex flex-col justify-between relative overflow-x-hidden">
      
      {/* ========================================================= */}
      {/* 0. FIXED FULL-BLEED HIGH-VISIBILITY VIDEO BACKGROUND       */}
      {/* ========================================================= */}
      {!videoError && (
        <div className="fixed inset-0 w-screen h-screen z-0 overflow-hidden pointer-events-none">
          <video
            autoPlay
            muted
            loop
            playsInline
            aria-hidden="true"
            onError={() => setVideoError(true)}
            className="w-full h-full object-cover opacity-100 filter contrast-105 saturate-110"
          >
            <source src="/videos/mplads-landing-bg.mp4" type="video/mp4" />
          </video>
          {/* Smooth seamless gradient overlay for video readability and bottom transition */}
          <div className="absolute inset-0 bg-gradient-to-b from-slate-950/20 via-transparent via-50% to-[#FAF8F5] pointer-events-none" />
        </div>
      )}

      {/* ========================================================= */}
      {/* 1. TOP MINIMAL GLASSMORPHIC NAVIGATION BAR                */}
      {/* ========================================================= */}
      <header className="sticky top-0 z-50 bg-[#FAF8F5]/70 backdrop-blur-md border-b border-slate-300/50 transition-all">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          
          {/* Left Logo / Branding */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center p-0.5 shadow-md border border-amber-400/50 group-hover:scale-105 transition-transform">
              <img src="/mplads-logo.png" alt="MPLADS Official Logo" className="w-full h-full object-contain rounded-full" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-serif font-bold text-[#0b192c] tracking-tight">
                  MPLADS AI
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium tracking-wide">
                Monitoring & Analytics Platform
              </p>
            </div>
          </Link>

          {/* Center Navigation Links */}
          <nav className="hidden md:flex items-center gap-7 text-sm font-medium text-slate-700">
            <button onClick={() => scrollToSection('hero')} className="hover:text-[#0b192c] transition-colors">Home</button>
            <button onClick={() => scrollToSection('about')} className="hover:text-[#0b192c] transition-colors">About</button>
            <button onClick={() => scrollToSection('data-freshness')} className="hover:text-[#0b192c] transition-colors font-semibold text-emerald-700 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Live Pipeline</span>
            </button>
            <button onClick={() => scrollToSection('how-it-works')} className="hover:text-[#0b192c] transition-colors">How It Works</button>
            <button onClick={() => scrollToSection('capabilities')} className="hover:text-[#0b192c] transition-colors">Analytics</button>
            <button onClick={() => scrollToSection('stakeholders')} className="hover:text-[#0b192c] transition-colors">Governance</button>
          </nav>

          {/* Right Action Gateway */}
          <div className="hidden sm:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link
                  to="/dashboard"
                  className="px-5 py-2.5 rounded-full bg-[#0b192c] hover:bg-[#1e3a8a] text-[#F8FAFC] text-xs font-semibold tracking-wide transition-all shadow-sm hover:shadow flex items-center gap-2"
                >
                  <LayoutDashboard className="w-4 h-4 text-[#f59e0b]" />
                  <span>Go to Dashboard</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
                <button
                  onClick={logout}
                  title="Sign Out"
                  className="p-2.5 rounded-full text-slate-500 hover:text-rose-700 hover:bg-rose-50 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="px-6 py-2.5 rounded-full bg-[#0b192c] hover:bg-[#1e3a8a] text-[#F8FAFC] text-xs font-bold tracking-wider uppercase transition-all shadow-sm hover:shadow-md flex items-center gap-2 group"
              >
                <span>LOGIN</span>
                <ArrowRight className="w-4 h-4 text-[#f59e0b] group-hover:translate-x-0.5 transition-transform" />
              </Link>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            {!isAuthenticated && (
              <Link
                to="/login"
                className="px-3.5 py-1.5 rounded-full bg-[#0b192c] text-[#F8FAFC] text-xs font-bold uppercase tracking-wider"
              >
                LOGIN →
              </Link>
            )}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-700 hover:bg-[#0b192c]/10"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-[#F8FAFC] border-b border-slate-200 px-4 pt-2 pb-6 space-y-3">
            <button onClick={() => scrollToSection('hero')} className="block w-full text-left py-2 text-sm font-medium text-slate-800">Home</button>
            <button onClick={() => scrollToSection('about')} className="block w-full text-left py-2 text-sm font-medium text-slate-800">About</button>
            <button onClick={() => scrollToSection('how-it-works')} className="block w-full text-left py-2 text-sm font-medium text-slate-800">How It Works</button>
            <button onClick={() => scrollToSection('capabilities')} className="block w-full text-left py-2 text-sm font-medium text-slate-800">Analytics</button>
            <button onClick={() => scrollToSection('stakeholders')} className="block w-full text-left py-2 text-sm font-medium text-slate-800">Governance</button>
            {isAuthenticated ? (
              <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)} className="block w-full text-center py-2.5 bg-[#0b192c] text-[#F8FAFC] rounded-xl text-xs font-bold uppercase tracking-wider">
                Go to Dashboard
              </Link>
            ) : (
              <Link to="/login" onClick={() => setMobileMenuOpen(false)} className="block w-full text-center py-2.5 bg-[#0b192c] text-[#F8FAFC] rounded-xl text-xs font-bold uppercase tracking-wider">
                LOGIN TO PORTAL →
              </Link>
            )}
          </div>
        )}
      </header>

      <main className="flex-1">
        {/* ========================================================= */}
        {/* 2. HERO SECTION (MINIMAL & ELEGANT)                        */}
        {/* ========================================================= */}
        <section id="hero" className="relative pt-12 pb-16 md:pt-16 md:pb-24 overflow-hidden z-10">
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
              
              {/* Left Column: Minimal Editorial Content */}
              <div className="lg:col-span-7 space-y-6">
                
                {/* Government Subhead Badge */}
                <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/90 backdrop-blur-md border border-slate-300/80 shadow-xs text-[#0b192c]">
                  <Landmark className="w-3.5 h-3.5 text-[#d97706]" />
                  <span className="text-[11px] font-semibold tracking-wide uppercase">
                    Ministry of Statistics & Programme Implementation (MoSPI)
                  </span>
                </div>

                {/* Main Headline */}
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-serif text-[#0b192c] leading-[1.12] tracking-tight">
                  <span className="text-[#0b192c] font-bold">
                    Smarter Monitoring.
                  </span>{' '}
                  <span className="block font-serif italic font-medium mt-1 text-amber-600 pb-1">
                    Stronger Public Infrastructure.
                  </span>
                </h1>

                {/* Crisp Concise Subtitle */}
                <p className="text-base sm:text-lg text-slate-800 font-medium leading-relaxed max-w-xl bg-white/85 backdrop-blur-sm p-4 rounded-2xl border border-slate-300 shadow-xs">
                  An AI-powered public governance monitoring platform designed to automatically surface cost anomalies, candidate duplicate works, fund flow bottlenecks, and statutory timeline delays across 773 districts nationwide.
                </p>

                {/* Stat Metrics Strip */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-xl">
                  <div className="bg-[#0b192c] text-white p-3 rounded-xl border border-slate-700 shadow-xs">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-amber-400">Total Sanctioned</p>
                    <p className="text-base font-serif font-bold mt-0.5">₹10,211 Cr</p>
                  </div>
                  <div className="bg-white/90 backdrop-blur-sm p-3 rounded-xl border border-slate-300 shadow-xs">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-[#0b192c]">Works Tracked</p>
                    <p className="text-base font-serif font-bold text-[#0b192c] mt-0.5">190,942</p>
                  </div>
                  <div className="bg-white/90 backdrop-blur-sm p-3 rounded-xl border border-slate-300 shadow-xs">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-[#0b192c]">Districts</p>
                    <p className="text-base font-serif font-bold text-[#0b192c] mt-0.5">773</p>
                  </div>
                  <div className="bg-white/90 backdrop-blur-sm p-3 rounded-xl border border-slate-300 shadow-xs">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-[#d97706]">AI Engines</p>
                    <p className="text-base font-serif font-bold text-[#0b192c] mt-0.5">4 Independent</p>
                  </div>
                </div>

                {/* Primary Action Buttons */}
                <div className="pt-2 flex flex-wrap items-center gap-3">
                  <button
                    onClick={() => scrollToSection('how-it-works')}
                    className="px-7 py-3 rounded-full bg-[#0b192c] hover:bg-[#1e3a8a] text-[#F8FAFC] text-xs font-semibold tracking-wide shadow-md transition-all flex items-center gap-2 group"
                  >
                    <span>Explore Platform</span>
                    <ArrowRight className="w-4 h-4 text-[#f59e0b] group-hover:translate-x-0.5 transition-transform" />
                  </button>

                  <Link
                    to="/login"
                    className="px-6 py-3 rounded-full bg-white hover:bg-slate-100 text-[#0b192c] border border-slate-300 text-xs font-semibold tracking-wide transition-all flex items-center gap-1.5 shadow-xs"
                  >
                    <span>Login to Portal</span>
                    <ChevronRight className="w-4 h-4 text-slate-400" />
                  </Link>
                </div>

              </div>

              {/* Right Column: Minimal Dark Analytical Card */}
              <div className="lg:col-span-5 flex justify-center">
                <div className="w-full max-w-md bg-gradient-to-b from-[#0b192c] via-[#0f243f] to-[#081220] backdrop-blur-xl rounded-3xl p-6 border border-white/15 shadow-2xl text-white space-y-5">
                  
                  {/* Card Header */}
                  <div className="flex items-center justify-between border-b border-white/15 pb-3">
                    <div className="flex items-center gap-2">
                      <Building2 className="w-4 h-4 text-[#f59e0b]" />
                      <span className="text-xs font-mono font-bold text-amber-200 tracking-wider">GOVERNANCE AI CORE</span>
                    </div>
                    <div className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-mono flex items-center gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span>LIVE AUDIT</span>
                    </div>
                  </div>

                  {/* Scheme Summary */}
                  <div className="bg-white/10 p-4 rounded-2xl border border-white/15 space-y-2">
                    <div className="flex items-center justify-between text-xs font-mono">
                      <span className="text-slate-300">Sanctioned Scope</span>
                      <span className="font-bold text-amber-300 text-sm">₹10,211.49 Cr</span>
                    </div>
                    <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
                      <div className="bg-amber-400 h-full w-[99.5%]" />
                    </div>
                    <div className="flex justify-between text-[11px] text-slate-300 pt-1">
                      <span>Disbursed: <strong className="text-emerald-300">₹10,166.10 Cr</strong></span>
                      <span>Works: <strong className="text-white">190,942</strong></span>
                    </div>
                  </div>

                  {/* 4 Models Badges */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-2.5 rounded-xl bg-white/10 text-xs">
                      <div className="flex items-center gap-2">
                        <TrendingUp className="w-3.5 h-3.5 text-amber-400" />
                        <span>Cost Anomaly Engine</span>
                      </div>
                      <span className="text-[10px] font-mono text-amber-200">IQR Benchmarking</span>
                    </div>

                    <div className="flex items-center justify-between p-2.5 rounded-xl bg-white/10 text-xs">
                      <div className="flex items-center gap-2">
                        <Copy className="w-3.5 h-3.5 text-amber-400" />
                        <span>Duplicate Detector</span>
                      </div>
                      <span className="text-[10px] font-mono text-amber-200">MiniLM-L6-v2</span>
                    </div>

                    <div className="flex items-center justify-between p-2.5 rounded-xl bg-white/10 text-xs">
                      <div className="flex items-center gap-2">
                        <Layers className="w-3.5 h-3.5 text-amber-400" />
                        <span>Fund Stagnation</span>
                      </div>
                      <span className="text-[10px] font-mono text-emerald-300">Tranche Flow</span>
                    </div>

                    <div className="flex items-center justify-between p-2.5 rounded-xl bg-white/10 text-xs">
                      <div className="flex items-center gap-2">
                        <Clock className="w-3.5 h-3.5 text-amber-400" />
                        <span>Delay SLA Engine</span>
                      </div>
                      <span className="text-[10px] font-mono text-amber-200">75d / 365d Rule</span>
                    </div>
                  </div>

                  {/* Footer caption */}
                  <div className="pt-2 border-t border-white/15 flex justify-between text-[11px] text-slate-400">
                    <span>Scheme Surveillance</span>
                    <span className="font-serif italic text-amber-200">MoSPI Govt of India</span>
                  </div>

                </div>
              </div>

            </div>
          </div>

          {/* Seamless Bottom Gradient Fade Transition */}
          <div className="absolute bottom-0 inset-x-0 h-36 bg-gradient-to-b from-transparent via-[#FAF8F5]/80 to-white pointer-events-none z-20" />
        </section>

        {/* ========================================================= */}
        {/* 3. ABOUT SECTION                                          */}
        {/* ========================================================= */}
        <section id="about" className="py-20 bg-white relative z-10 border-b border-slate-200/80 shadow-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mb-10">
              <span className="text-xs font-bold uppercase tracking-widest text-[#d97706]">
                Institutional Context
              </span>
              <h2 className="text-2xl sm:text-4xl font-serif text-[#0b192c] mt-1 leading-tight">
                Enhancing MPLADS Oversight Through Explainable AI.
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-slate-700 leading-relaxed text-sm">
              <div className="bg-[#FAF8F5] p-7 rounded-2xl border border-slate-300 shadow-xs space-y-3">
                <div className="w-9 h-9 rounded-xl bg-[#0b192c] text-[#f59e0b] flex items-center justify-center">
                  <Building2 className="w-4 h-4" />
                </div>
                <h3 className="text-base font-bold text-[#0b192c]">The Governance Challenge</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  The MPLADS scheme enables Members of Parliament to recommend local developmental works nationwide. Executing thousands of projects across 861 districts requires automated risk indicators to support administrative review.
                </p>
              </div>

              <div className="bg-[#FAF8F5] p-7 rounded-2xl border border-slate-300 shadow-xs space-y-3">
                <div className="w-9 h-9 rounded-xl bg-[#0b192c] text-[#f59e0b] flex items-center justify-center">
                  <Sparkles className="w-4 h-4" />
                </div>
                <h3 className="text-base font-bold text-[#0b192c]">The Analytical Solution</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Four independent machine learning and rule engines evaluate cost distributions, text semantics, payment tranches, and statutory timelines to surface potential risk flags for targeted field verification.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* ========================================================= */}
        {/* LIVE DATA SCRAPER & AUTO-UPDATE PIPELINE SECTION           */}
        {/* ========================================================= */}
        <section id="data-freshness" className="py-20 bg-gradient-to-b from-white via-[#FAF8F5] to-white relative z-10 border-b border-slate-200/80 shadow-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="text-center max-w-3xl mx-auto mb-14">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 font-mono text-xs font-bold mb-3">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>REAL-TIME DATA FRESHNESS PIPELINE</span>
              </div>
              <h2 className="text-3xl sm:text-4xl font-serif text-[#0b192c] leading-tight">
                Always Up-to-Date. Direct Official Integration.
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 font-medium mt-3 leading-relaxed max-w-2xl mx-auto">
                Our production-grade live scraper continuously connects to the official government dashboard, validating, normalizing, and trigger-updating all 190,942+ works in real time without destroying historical records.
              </p>
            </div>

            {/* Pipeline Architecture Diagram & Highlights */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              
              {/* Left Column: Interactive Flow Steps */}
              <div className="lg:col-span-7 space-y-4">
                
                {/* Step 1: Target Portal */}
                <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4 hover:border-amber-400/60 transition-all">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 border border-blue-200 flex items-center justify-center shrink-0 font-bold">
                    <Globe className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-[#0b192c]">1. Official Website Live Connector</h4>
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">Scrapling Engine</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      Automatically queries <code className="text-amber-800 font-mono font-bold">mplads.mospi.gov.in</code> for new MP recommendations, administrative sanctions, completion certificates, and expenditure vouchers.
                    </p>
                  </div>
                </div>

                {/* Step 2: Immutable Snapshot */}
                <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4 hover:border-amber-400/60 transition-all">
                  <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 border border-purple-200 flex items-center justify-center shrink-0 font-bold">
                    <Database className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-[#0b192c]">2. Immutable Raw Snapshot Archiving</h4>
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-purple-100 text-purple-800">SHA-256 Lineage</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      Saves full raw HTML/JSON snapshots under timestamped paths (<code className="text-amber-800 font-mono">data/raw/live_source/</code>) with cryptographic hash integrity and full audit lineage.
                    </p>
                  </div>
                </div>

                {/* Step 3: Validation & Canonical Merge */}
                <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4 hover:border-amber-400/60 transition-all">
                  <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-200 flex items-center justify-center shrink-0 font-bold">
                    <CheckCircle2 className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-[#0b192c]">3. Schema Validation & Normalization</h4>
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">Zero Data Loss</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      Validates financial numeric bounds, normalizes Indian Rupee currency formats, parses dates, and safely upserts new records while preserving historical records.
                    </p>
                  </div>
                </div>

                {/* Step 4: Selective ML Retrigger */}
                <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex items-start gap-4 hover:border-amber-400/60 transition-all">
                  <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 border border-amber-200 flex items-center justify-center shrink-0 font-bold">
                    <Zap className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-[#0b192c]">4. Selective 4-Model ML Auto-Trigger</h4>
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-900">Sub-Second Execution</span>
                    </div>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      Detects changed fields and re-evaluates Cost Anomaly, Duplicate Work Candidate Pairs, Fund Stagnation, and Delay SLA breaches instantly.
                    </p>
                  </div>
                </div>

              </div>

              {/* Right Column: Live Data Pipeline Monitor Card */}
              <div className="lg:col-span-5 bg-[#0b192c] text-white p-6 sm:p-7 rounded-3xl border border-white/15 shadow-2xl space-y-5">
                <div className="flex items-center justify-between border-b border-white/15 pb-3">
                  <div className="flex items-center gap-2">
                    <RefreshCw className="w-4 h-4 text-amber-400 animate-spin" />
                    <span className="text-xs font-mono font-bold text-amber-300 tracking-wider">LIVE INGESTION PIPELINE</span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[10px] font-mono border border-emerald-500/30">
                    ACTIVE SENSOR
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="p-3.5 rounded-xl bg-white/10 border border-white/10 flex justify-between items-center text-xs">
                    <span className="text-slate-300">Official Portal Target</span>
                    <span className="font-mono text-amber-200 font-bold truncate max-w-[180px]">mplads.mospi.gov.in</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white/10 border border-white/10 flex justify-between items-center text-xs">
                    <span className="text-slate-300">Raw Snapshot Storage</span>
                    <span className="font-mono text-emerald-300 font-bold">Immutable SHA256</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white/10 border border-white/10 flex justify-between items-center text-xs">
                    <span className="text-slate-300">Canonical Dataset</span>
                    <span className="font-mono text-white font-bold">190,942 Verified Works</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white/10 border border-white/10 flex justify-between items-center text-xs">
                    <span className="text-slate-300">Model Re-evaluation</span>
                    <span className="font-mono text-amber-300 font-bold">Automatic Selective</span>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-200 text-xs leading-relaxed space-y-1">
                  <p className="font-bold text-white flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-amber-400" />
                    Source Telemetry & Admin Console
                  </p>
                  <p className="text-[11px] text-slate-300">
                    Ministry administrators can track live scraper health, view SHA-256 snapshot lineage, and trigger manual on-demand synchronization directly from the <code className="text-amber-200 font-mono">Data Source Monitor</code>.
                  </p>
                </div>
              </div>

            </div>

          </div>
        </section>

        {/* ========================================================= */}
        {/* 4. HOW IT WORKS SECTION                                   */}
        {/* ========================================================= */}
        <section id="how-it-works" className="py-16 bg-[#FAF8F5]/90 backdrop-blur-md relative z-10 border-b border-slate-300/80 shadow-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-bold uppercase tracking-widest text-[#d97706]">
                Workflow & Pipeline
              </span>
              <h2 className="text-2xl sm:text-4xl font-serif text-[#0b192c] mt-1 leading-tight">
                From Data Ingestion to Audit Insights.
              </h2>
            </div>

            {/* 4 Steps Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              
              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-10 h-10 rounded-xl bg-[#0b192c] text-[#F8FAFC] flex items-center justify-center font-bold text-xs">
                  01
                </div>
                <h3 className="text-base font-bold text-[#0b192c]">COLLECT</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Work proposals, sanction orders, transaction vouchers, and progress records enter the pipeline automatically.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-10 h-10 rounded-xl bg-[#0b192c] text-[#F8FAFC] flex items-center justify-center font-bold text-xs">
                  02
                </div>
                <h3 className="text-base font-bold text-[#0b192c]">ANALYZE</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Analytical models evaluate cost distributions, text semantics, payment tranches, and statutory dates.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-10 h-10 rounded-xl bg-[#0b192c] text-[#F8FAFC] flex items-center justify-center font-bold text-xs">
                  03
                </div>
                <h3 className="text-base font-bold text-[#0b192c]">IDENTIFY</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Surfaces cost estimate anomalies, candidate duplicate works, expenditure bottlenecks, and SLA breaches.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-10 h-10 rounded-xl bg-[#0b192c] text-[#F8FAFC] flex items-center justify-center font-bold text-xs">
                  04
                </div>
                <h3 className="text-base font-bold text-[#0b192c]">PRIORITIZE</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Presents ranked risk signals in specialized governance dashboards to support administrative audit review.
                </p>
              </div>

            </div>

          </div>
        </section>

        {/* ========================================================= */}
        {/* 5. FOUR ANALYTICAL CAPABILITIES                           */}
        {/* ========================================================= */}
        <section id="capabilities" className="py-20 bg-[#0b192c] text-[#F8FAFC] relative z-10 border-b border-amber-500/20 shadow-xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="max-w-3xl mb-12">
              <span className="text-xs font-bold uppercase tracking-widest text-[#f59e0b]">
                Analytical Engine Architecture
              </span>
              <h2 className="text-2xl sm:text-4xl font-serif mt-1 leading-tight">
                Four Signals. One Clearer View.
              </h2>
            </div>

            {/* 4 Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              <div className="p-6 rounded-2xl bg-[#0f243f] border border-white/15 space-y-3">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <span className="text-xs font-mono font-bold text-[#f59e0b]">01 — COST ANOMALY</span>
                  <TrendingUp className="w-4 h-4 text-amber-400" />
                </div>
                <h3 className="text-lg font-serif text-white">Peer-Relative Cost Benchmark</h3>
                <p className="text-slate-300 text-xs leading-relaxed">
                  Evaluates project costs using hierarchical Isolation Forest and IQR norms, benchmarking estimates against district and category medians.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-[#0f243f] border border-white/15 space-y-3">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <span className="text-xs font-mono font-bold text-[#f59e0b]">02 — DUPLICATE DETECTOR</span>
                  <Copy className="w-4 h-4 text-amber-400" />
                </div>
                <h3 className="text-lg font-serif text-white">Semantic & Proximity Analysis</h3>
                <p className="text-slate-300 text-xs leading-relaxed">
                  Leverages sentence transformers (<code className="text-amber-200">MiniLM-L6-v2</code>) and temporal blocking to surface candidate duplicate project sanctions.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-[#0f243f] border border-white/15 space-y-3">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <span className="text-xs font-mono font-bold text-[#f59e0b]">03 — FUND & EXPENDITURE</span>
                  <Layers className="w-4 h-4 text-amber-400" />
                </div>
                <h3 className="text-lg font-serif text-white">Disbursement & Payment Diagnostics</h3>
                <p className="text-slate-300 text-xs leading-relaxed">
                  Monitors financial flows using Herfindahl-Hirschman Index (HHI), flagging payment tranche concentration and dormant sanctions.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-[#0f243f] border border-white/15 space-y-3">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <span className="text-xs font-mono font-bold text-[#f59e0b]">04 — DELAY & SLA ENGINE</span>
                  <Clock className="w-4 h-4 text-amber-400" />
                </div>
                <h3 className="text-lg font-serif text-white">Statutory Timeline Compliance</h3>
                <p className="text-slate-300 text-xs leading-relaxed">
                  Deterministic rule engine enforcing statutory limits: 75-day recommendation-to-sanction SLA (Para 3.12) and 365-day work execution windows.
                </p>
              </div>

            </div>

          </div>
        </section>

        {/* ========================================================= */}
        {/* 6. MULTI-TIER GOVERNANCE SECTION                          */}
        {/* ========================================================= */}
        <section id="stakeholders" className="py-16 bg-[#FAF8F5]/90 backdrop-blur-md relative z-10 border-b border-slate-300/80 shadow-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-bold uppercase tracking-widest text-[#d97706]">
                Institutional Scoping
              </span>
              <h2 className="text-2xl sm:text-4xl font-serif text-[#0b192c] mt-1">
                Built for Multi-Tier Public Governance.
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              
              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-9 h-9 rounded-xl bg-[#0b192c] text-white flex items-center justify-center">
                  <Landmark className="w-4 h-4 text-[#f59e0b]" />
                </div>
                <h3 className="text-sm font-bold text-[#0b192c]">CENTRAL MINISTRY</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  National-level oversight across all 36 States/UTs, macro-level fund tracking, and systemic risk reviews.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-9 h-9 rounded-xl bg-[#0b192c] text-white flex items-center justify-center">
                  <Building2 className="w-4 h-4 text-[#f59e0b]" />
                </div>
                <h3 className="text-sm font-bold text-[#0b192c]">STATE OFFICERS</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  State-wide visibility across assigned districts, tracking inter-district cost variances and sanction backlogs.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-9 h-9 rounded-xl bg-[#0b192c] text-white flex items-center justify-center">
                  <ShieldCheck className="w-4 h-4 text-[#f59e0b]" />
                </div>
                <h3 className="text-sm font-bold text-[#0b192c]">DISTRICT OFFICERS</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Operational monitoring within assigned district boundaries, auditing cost estimates and vendor billings.
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-slate-300 shadow-xs space-y-3">
                <div className="w-9 h-9 rounded-xl bg-[#0b192c] text-white flex items-center justify-center">
                  <FileSearch className="w-4 h-4 text-[#f59e0b]" />
                </div>
                <h3 className="text-sm font-bold text-[#0b192c]">MEMBERS OF PARLIAMENT</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Real-time scrutiny into recommended constituency works, tracking sanction velocity and fund releases.
                </p>
              </div>

            </div>

            {/* ========================================================= */}
            {/* SECURITY & COMPLIANCE ARCHITECTURE SECTION               */}
            {/* ========================================================= */}
            <div id="security" className="mt-16 pt-12 border-t border-slate-200">
              <div className="text-center max-w-3xl mx-auto mb-10">
                <span className="text-xs font-bold uppercase tracking-widest text-[#d97706]">
                  Enterprise Security & Privacy
                </span>
                <h2 className="text-2xl sm:text-3xl font-serif text-[#0b192c] mt-1">
                  Built for Government Grade Scoping & Compliance
                </h2>
                <p className="text-xs text-slate-600 mt-2">
                  Multi-layered security protocol protecting national financial records, administrative logs, and user credentials.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2.5">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
                    <Shield className="w-4 h-4" />
                  </div>
                  <h4 className="text-sm font-bold text-[#0b192c]">PostgreSQL RLS Scoping</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Row-Level Security policies cryptographically scope queries based on assigned state, district, or MP portfolio boundaries.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2.5">
                  <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
                    <Lock className="w-4 h-4" />
                  </div>
                  <h4 className="text-sm font-bold text-[#0b192c]">Zero Secret Exposure</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    All AI API keys and database credentials reside strictly in server-side <code className="font-mono text-purple-900 bg-purple-50 px-1 py-0.5 rounded text-[10px]">.env</code> storage, zero client bundle exposure.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2.5">
                  <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                    <BarChart3 className="w-4 h-4" />
                  </div>
                  <h4 className="text-sm font-bold text-[#0b192c]">Audit Trail & Rate Limits</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Every data ingestion run logs SHA-256 snapshots, changed field diffs, and enforces anti-DDoS SlowAPI rate limiting.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2.5">
                  <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
                    <HelpCircle className="w-4 h-4" />
                  </div>
                  <h4 className="text-sm font-bold text-[#0b192c]">Anti-Prompt Injection AI</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Subho AI Assistant applies regex inspection and server-side RBAC prompts to prevent unauthorized access or secret leaks.
                  </p>
                </div>
              </div>
            </div>

            {/* ========================================================= */}
            {/* FREQUENTLY ASKED QUESTIONS (FAQ) ACCORDION               */}
            {/* ========================================================= */}
            <div id="faq" className="mt-16 pt-12 border-t border-slate-200 max-w-4xl mx-auto">
              <div className="text-center mb-10">
                <span className="text-xs font-bold uppercase tracking-widest text-[#d97706]">
                  Knowledge Base & Guidance
                </span>
                <h2 className="text-2xl sm:text-3xl font-serif text-[#0b192c] mt-1">
                  Frequently Asked Questions
                </h2>
              </div>

              <div className="space-y-3">
                {[
                  {
                    q: "How does the platform maintain data accuracy and freshness?",
                    a: "Our production Scrapling Live Scraper engine periodically checks the official government portal (mplads.mospi.gov.in) for new recommendations, sanctions, completions, and disbursements. Each raw pull is archived with SHA-256 hash lineage, normalized, and updated in real time without destroying historical records."
                  },
                  {
                    q: "How does Model 2 detect duplicate work candidate pairs?",
                    a: "Model 2 applies strict spatial-temporal blocking (same district, same category, within 90-day sanction windows and ±10% amount similarity). Candidate work pairs are then evaluated using MiniLM-L6-v2 semantic vector embeddings and cosine text similarity."
                  },
                  {
                    q: "What statutory SLA timelines are monitored under Model 4?",
                    a: "Model 4 enforces statutory rules established by MPLADS guidelines, including the 75-day SLA from recommendation date to sanction order (Para 3.12 Guidelines) and the 365-day execution completion SLA for open ongoing works."
                  },
                  {
                    q: "How does Subho AI assist different stakeholder roles?",
                    a: "Subho AI is a role-aware conversational assistant. When logged in as a Central Ministry official, State Nodal Officer, District Officer, or Member of Parliament, Subho AI automatically tailors its context to your assigned jurisdiction while keeping data secure."
                  }
                ].map((faq, index) => (
                  <div
                    key={index}
                    className="border border-slate-300 rounded-2xl bg-white overflow-hidden shadow-xs transition-all"
                  >
                    <button
                      onClick={() => setOpenFaq(openFaq === index ? null : index)}
                      className="w-full px-6 py-4 text-left flex items-center justify-between font-semibold text-xs sm:text-sm text-[#0b192c] hover:bg-slate-50 transition-colors"
                    >
                      <span>{faq.q}</span>
                      {openFaq === index ? (
                        <ChevronUp className="w-4 h-4 text-amber-600 shrink-0" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                      )}
                    </button>
                    {openFaq === index && (
                      <div className="px-6 pb-4 pt-1 text-xs text-slate-600 leading-relaxed border-t border-slate-100 bg-slate-50/50">
                        {faq.a}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Gateway CTA Banner */}
            <div className="mt-14 p-7 rounded-3xl bg-[#0b192c] text-[#F8FAFC] flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
              <div>
                <h3 className="text-xl font-serif text-white">Ready to Access the Gateway?</h3>
                <p className="text-amber-100/90 text-xs mt-1">
                  Authenticate with authorized government credentials to enter the protected analytics workspace.
                </p>
              </div>
              <Link
                to="/login"
                className="px-7 py-3 rounded-full bg-[#d97706] hover:bg-[#b45309] text-white text-xs font-bold uppercase tracking-wider shadow-md transition-all shrink-0 flex items-center gap-2"
              >
                <span>PROCEED TO LOGIN</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

          </div>
        </section>
      </main>

      {/* ========================================================= */}
      {/* 7. PUBLIC LANDING PAGE FOOTER                             */}
      {/* ========================================================= */}
      <footer className="bg-[#071322] text-[#F8FAFC]/80 py-10 border-t border-white/10 relative z-10 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center pb-6 border-b border-white/10">
            
            <div className="md:col-span-6 space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center p-0.5 border border-amber-400/50 shadow-md">
                  <img src="/mplads-logo.png" alt="MPLADS Official Logo" className="w-full h-full object-contain rounded-full" />
                </div>
                <span className="text-lg font-serif font-bold text-white tracking-tight">MPLADS AI</span>
              </div>
              <p className="text-xs text-slate-400 max-w-md">
                AI-assisted monitoring and analytics platform for Member of Parliament Local Area Development Scheme implementation.
              </p>
            </div>

            <div className="md:col-span-6 flex flex-wrap gap-6 md:justify-end text-xs font-medium text-slate-300">
              <button onClick={() => scrollToSection('hero')} className="hover:text-amber-300 transition-colors">Home</button>
              <button onClick={() => scrollToSection('about')} className="hover:text-amber-300 transition-colors">About</button>
              <button onClick={() => scrollToSection('how-it-works')} className="hover:text-amber-300 transition-colors">How It Works</button>
              <button onClick={() => scrollToSection('capabilities')} className="hover:text-amber-300 transition-colors">Analytics</button>
              <Link to="/login" className="text-amber-400 font-bold hover:underline">Login Gateway →</Link>
            </div>

          </div>

          <div className="pt-6 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-400 gap-4 font-mono">
            <div>
              सांख्यिकी और कार्यक्रम कार्यान्वयन मंत्रालय • Ministry of Statistics & Programme Implementation
            </div>
            <div className="flex items-center gap-4">
              <span>© {new Date().getFullYear()} MPLADS AI. All rights reserved.</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};
