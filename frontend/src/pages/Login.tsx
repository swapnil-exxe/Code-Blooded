import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth, CANONICAL_DEMO_ACCOUNTS } from '@/context/AuthContext';
import { Role } from '@/types/auth';
import {
  Lock,
  Mail,
  ArrowRight,
  AlertCircle,
  Landmark,
  ArrowLeft,
  ShieldCheck,
  Zap,
  Eye,
  EyeOff,
} from 'lucide-react';

export const Login: React.FC = () => {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const passwordInputRef = useRef<HTMLInputElement>(null);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [videoError, setVideoError] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setError(null);
    setLoading(true);

    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch (err: any) {
      const status = err?.response?.status;
      let msg = 'Invalid credentials. Please check your credentials and try again.';
      if (status === 429) {
        msg = 'Too many unsuccessful attempts. Please try again later.';
      }
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectRole = (demoEmail: string) => {
    setError(null);
    setEmail(demoEmail);
    if (passwordInputRef.current) {
      passwordInputRef.current.focus();
    }
  };

  return (
    <div className="fixed inset-0 w-screen h-screen overflow-hidden bg-[#0b192c] text-white font-sans selection:bg-[#f59e0b]/30 selection:text-white flex flex-col justify-between">
      {/* 1. FULL-BLEED UNTOUCHED VIDEO BACKGROUND */}
      {!videoError ? (
        <video
          autoPlay
          muted
          loop
          playsInline
          aria-hidden="true"
          onError={() => setVideoError(true)}
          className="fixed inset-0 w-full h-full object-cover z-0 pointer-events-none"
        >
          <source src="/videos/mplads-login-bg.mp4" type="video/mp4" />
        </video>
      ) : (
        <div className="fixed inset-0 bg-gradient-to-br from-[#0b192c] via-[#0f243f] to-[#081220] z-0" />
      )}

      {/* 2. ULTRA-SUBTLE OVERLAY LAYER */}
      <div className="fixed inset-0 z-1 bg-black/20 pointer-events-none" />

      {/* 3. INTERACTIVE CONTENT LAYER */}
      <div className="relative z-10 flex flex-col justify-between h-full w-full pointer-events-auto overflow-y-auto">
        {/* Floating Transparent Header */}
        <header className="px-6 sm:px-10 py-4 w-full shrink-0">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <Link
              to="/"
              className="flex items-center gap-2 text-xs font-semibold text-slate-200 hover:text-amber-400 transition-colors group px-3.5 py-1.5 rounded-full bg-black/25 backdrop-blur-md border border-white/15"
            >
              <ArrowLeft className="w-4 h-4 text-[#f59e0b] group-hover:-translate-x-0.5 transition-transform" />
              <span>Back to Public Landing Page</span>
            </Link>

            <div className="hidden sm:flex items-center gap-2 px-4 py-1.5 rounded-full bg-black/25 backdrop-blur-md border border-white/15 text-[11px] font-mono text-amber-200">
              <Landmark className="w-3.5 h-3.5 text-[#f59e0b]" />
              <span>सांख्यिकी और कार्यक्रम कार्यान्वयन मंत्रालय • Ministry of Statistics</span>
            </div>

            <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-black/25 backdrop-blur-md border border-white/15">
              <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center shrink-0 p-0.5 border border-amber-400/50 shadow-md">
                <img src="/mplads-logo.png" alt="MPLADS Official Logo" className="w-full h-full object-contain rounded-full" />
              </div>
              <span className="text-xs font-serif font-bold text-white tracking-wide">MPLADS AI</span>
            </div>
          </div>
        </header>

        {/* HIGH-TRANSPARENCY LIQUID GLASS CONTAINER */}
        <main className="flex-1 flex items-center justify-center max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 my-auto">
          <div className="w-full bg-[#0b192c]/25 backdrop-blur-xl border border-white/20 rounded-3xl p-6 sm:p-8 lg:p-10 shadow-2xl my-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            {/* LEFT COLUMN: APPLICATION ROLES GUIDANCE */}
            <div className="lg:col-span-7 space-y-5">
              <div className="space-y-1.5">
                <div className="inline-flex items-center gap-2 text-[10px] font-mono font-bold tracking-widest uppercase text-amber-300 px-3 py-1 rounded-full bg-[#f59e0b]/20 border border-[#f59e0b]/30 backdrop-blur-md">
                  <Zap className="w-3 h-3 text-[#f59e0b]" />
                  SELECT OFFICIAL ROLE TO SIGN IN
                </div>
                <h2 className="text-2xl sm:text-3xl font-serif font-bold text-white tracking-tight drop-shadow-md">
                  MPLADS AI Surveillance Gateway
                </h2>
                <p className="text-xs text-slate-200 leading-relaxed max-w-xl drop-shadow-sm">
                  Select any of the official stakeholder role profiles below to select your account email, then enter your authorized credentials on the right.
                </p>
              </div>

              {/* 4 STAKEHOLDER ROLE CARDS */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                {CANONICAL_DEMO_ACCOUNTS.map((acc) => (
                  <button
                    key={acc.role}
                    type="button"
                    onClick={() => handleSelectRole(acc.email)}
                    disabled={loading}
                    className="flex flex-col justify-between text-left p-4 rounded-2xl bg-black/25 hover:bg-black/45 backdrop-blur-md border border-white/20 hover:border-amber-400/60 transition-all duration-200 group cursor-pointer relative overflow-hidden shadow-lg"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded bg-amber-400/25 border border-amber-400/40 text-amber-200">
                        {acc.role}
                      </span>
                      <span className="text-[11px] font-medium text-amber-300 group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                        <span>Select Role</span>
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                    <div>
                      <div className="text-xs font-bold text-white group-hover:text-amber-200 transition-colors">
                        {acc.label}
                      </div>
                      <div className="text-[11px] font-mono text-slate-300 truncate mt-0.5">
                        {acc.email}
                      </div>
                    </div>
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-3 p-3.5 rounded-xl bg-black/30 backdrop-blur-md border border-amber-400/30 text-xs text-amber-200/90 font-mono shadow-md">
                <ShieldCheck className="w-4 h-4 text-[#f59e0b] shrink-0" />
                <span>Authoritative Server Authentication: <strong>PostgreSQL Password Hash Verification</strong></span>
              </div>
            </div>

            {/* RIGHT COLUMN: MANUAL LOGIN FORM */}
            <div className="lg:col-span-5 bg-black/25 backdrop-blur-md border border-white/20 rounded-2xl p-6 sm:p-8 space-y-5 shadow-xl">
              <div>
                <div className="inline-block text-[10px] font-mono font-bold tracking-widest uppercase text-amber-300 px-2.5 py-1 rounded-md bg-[#f59e0b]/20 border border-[#f59e0b]/30 mb-2">
                  RESTRICTED ACCESS
                </div>
                <h3 className="text-xl font-serif text-white font-bold">Officer Sign In</h3>
                <p className="text-xs text-slate-300 mt-1">Enter your credentials to access the system.</p>
              </div>

              {error && (
                <div className="p-3.5 rounded-xl bg-rose-500/25 border-2 border-rose-500/60 text-rose-100 text-xs flex items-center gap-3 shadow-lg backdrop-blur-md">
                  <AlertCircle className="w-5 h-5 shrink-0 text-rose-400" />
                  <div className="space-y-0.5">
                    <div className="font-bold text-rose-200 uppercase tracking-wider text-[10px]">Authentication Error</div>
                    <div className="font-medium text-slate-100">{error}</div>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-[11px] font-mono font-bold uppercase tracking-wider text-slate-200 mb-1.5">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                    <input
                      id="login-email"
                      name="email"
                      autoComplete="username"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="e.g. officer@mplads.gov.in"
                      required
                      className="w-full bg-white/10 border border-white/20 focus:border-[#f59e0b] focus:ring-2 focus:ring-[#f59e0b]/30 text-white placeholder-slate-400 rounded-xl pl-10 pr-4 py-3 text-xs font-medium transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-mono font-bold uppercase tracking-wider text-slate-200 mb-1.5">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                    <input
                      id="login-password"
                      name="password"
                      autoComplete="current-password"
                      ref={passwordInputRef}
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter password"
                      required
                      className="w-full bg-white/10 border border-white/20 focus:border-[#f59e0b] focus:ring-2 focus:ring-[#f59e0b]/30 text-white placeholder-slate-400 rounded-xl pl-10 pr-10 py-3 text-xs font-medium transition-all"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-3 text-slate-400 hover:text-amber-400 transition-colors p-0.5 rounded cursor-pointer"
                      title={showPassword ? "Hide password" : "Show password"}
                      aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                      {showPassword ? (
                        <EyeOff className="w-4 h-4" />
                      ) : (
                        <Eye className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full mt-2 py-3.5 px-6 bg-gradient-to-r from-[#d97706] to-[#f59e0b] hover:from-[#b45309] hover:to-[#d97706] text-[#0b192c] font-bold rounded-xl text-xs sm:text-sm shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50 group cursor-pointer"
                >
                  <span>{loading ? 'Signing in...' : 'Sign In'}</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </button>
              </form>
            </div>

          </div>
        </main>

        {/* Seamless Floating Footer */}
        <footer className="py-4 w-full text-center text-[11px] text-slate-300 shrink-0">
          <span className="px-4 py-1.5 rounded-full bg-black/25 backdrop-blur-md border border-white/15 inline-block">
            Government of India • Ministry of Statistics and Programme Implementation (MoSPI)
          </span>
        </footer>
      </div>
    </div>
  );
};
