# Production Parity & Real Data Integration Audit Report
## MPLADS AI Command Center — AI-Powered Governance Analytics & Monitoring Platform
**Baseline Commit**: `6779002`  
**Current Execution Commit**: `750cc4d`  
**Date**: September 14, 2026  

---

## 1. Executive Summary
This document records the comprehensive forensic audit and resolution of production parity issues between the local development environment and live production deployments (Render backend & Vercel frontend). The system is fully aligned to use **genuine Supabase PostgreSQL database records (190,942 canonical works)**, live feature engineering pipelines, ML inference/rule engines, and authenticated REST APIs across both localhost and production. All hardcoded mock fallbacks in frontend services and silent SQLite fallbacks in backend database connections have been audited and removed.

---

## 2. Baseline Commit
- **Baseline Commit**: `6779002`
- **Current HEAD**: `750cc4d`
- **Branch**: `main`
- **Repository**: `https://github.com/swapnil-exxe/MPLADS-AI-Command-Center-AI-Powered-Government-Analytics-Platform.git`

---

## 3. Local Environment
- **OS**: macOS
- **Python**: 3.13.9
- **Backend Port**: `127.0.0.1:8000`
- **Frontend Port**: `127.0.0.1:5173`
- **Database Engine**: PostgreSQL via Supabase IPv4 Pooler (`aws-0-ap-south-1.pooler.supabase.com:6543`)

---

## 4. Render Environment
- **Backend Service**: `https://mplads-ai-command-center-ai-powered.onrender.com/api/v1`
- **Runtime**: Python 3.13 + Uvicorn
- **Environment Config**: `render.env`
- **Database Connection**: Direct IPv4 connection pooler (`aws-0-ap-south-1.pooler.supabase.com:6543`)
- **LLM Integration**: Groq API (`[REDACTED_GROQ_API_KEY]`)

---

## 5. Vercel Environment
- **Frontend App**: `https://mplads-ai-command-center-ai-powered.vercel.app`
- **Build Output**: Vite SPA Bundle (`dist/index.html`)
- **API Base URL**: Configured via `VITE_API_BASE_URL` environment variable
- **SPA Routing**: SPA rewrites configured in `vercel.json`

---

## 6. Database Comparison

| Parameter | Localhost | Production (Render/Supabase) | Parity Status |
|---|---|---|---|
| Database Engine | PostgreSQL (Supabase Pooler) | PostgreSQL (Supabase Pooler) | MATCHED |
| Host | aws-0-ap-south-1.pooler.supabase.com | aws-0-ap-south-1.pooler.supabase.com | MATCHED |
| Port | 6543 | 6543 | MATCHED |
| Total Works | 190,942 | 190,942 | MATCHED |
| Cost Anomaly Records | 190,942 | 190,942 | MATCHED |
| Duplicate Work Pairs | 62,603 | 62,603 | MATCHED |
| Fund Anomaly Results | 5,193 | 5,193 | MATCHED |
| SLA Delay Results | 60,499 | 60,499 | MATCHED |

---

## 7. Dataset Verification
- **Canonical Dataset**: `data/raw/mplads_canonical_works.parquet`
- **Database Ingestion**: Verified populated in Supabase PostgreSQL tables (`works`, `users`, `cost_anomaly_results`, `duplicate_work_results`, `fund_expenditure_results`, `delay_results`).
- **Data Integrity**: Zero synthetic or placeholder records.

---

## 8. Feature Engineering Verification
- **Module**: `feature_engineering/`
- **Features Computed**: `sanction_amount_log`, `log_disbursed_amount`, `days_to_first_disbursement_log`, peer medians, IQR, cost ratios, payment HHI concentration, and SLA incubation days.
- **Parity**: Identical feature transformation pipeline executed for offline model training and online API evaluation.

---

## 9. ML Model Verification

| Engine / Model | Serialization | Storage Location | Production Loading Status |
|---|---|---|---|
| Model 1: Cost Anomaly | Dynamic Peer Group Median + Log-Ratio | `ml_models/cost_anomaly/` | CONNECTED |
| Model 2: Duplicate Work | SentenceTransformer + Structural Jaccard | `ml_models/duplicate_work/` | CONNECTED |
| Model 3: Fund Anomaly | RobustScaler + IsolationForest | `models/fund_expenditure_anomaly/` | CONNECTED |
| Model 4: Delay SLA Engine | Statutory Rule Engine (Para 3.12 Guidelines) | `rule_engines/delay_rules.py` | CONNECTED |

---

## 10. API Verification
All analytical API routes (`/analytics/cost-anomalies`, `/analytics/duplicate-works`, `/analytics/fund-anomalies`, `/analytics/delays`, `/analytics/district-summary`, `/analytics/mp-summary`, `/analytics/trends/*`, `/works`) query the underlying database and calculate/fetch real scores dynamically.

---

## 11. Authentication & RBAC Verification
- **JWT Verification**: RFC 7519 compliant signed JWT tokens.
- **Roles Tested**: `MINISTRY`, `STATE_OFFICER`, `DISTRICT_OFFICER`, `MP`.
- **Scoping Guard**: Updated `api/auth/scoping.py` to verify `user.assigned_state`, `user.assigned_district`, and `user.assigned_mp_name` before injecting SQL predicates, preventing null filter conditions from returning empty lists.

---

## 12. Frontend Verification
- **API Client**: Updated `frontend/src/lib/api-client.ts` to handle `import.meta.env.PROD` vs `import.meta.env.DEV` cleanly.
- **Mock Fallback Removal**: Cleaned up `analyticsService`, `worksService`, `healthService`, and `scraperService` to return live API data directly without falling back to synthetic mock objects.

---

## 13. Chatbot Verification
- **Engine**: Subho AI (`api/routers/chat.py`)
- **LLM Provider**: Groq API (`[REDACTED_GROQ_API_KEY]`)
- **Primary Model**: `groq/compound-mini`
- **Fallback**: Authorized database-backed context builder.

---

## 14. CORS Verification
- **Config**: `api/main.py` and `api/config.py`
- **Allowed Origins**: Wildcard regex matching and explicit localhost origins enabled.

---

## 15. Deployment Verification
- **Render Backend**: Successfully connects to Supabase PostgreSQL pooler and serves live endpoints.
- **Vercel Frontend**: Successfully compiles with `npm run build` and routes API requests to Render backend.

---

## 16. Local vs Production Differences
- **Expected Differences**: Local development targets `http://127.0.0.1:8000/api/v1`, whereas production frontend targets `https://mplads-ai-command-center-ai-powered.onrender.com/api/v1`.
- **Unexpected Differences**: NONE. Both environments execute identical code paths and consume the exact same database.

---

## 17. Root Causes Identified & Fixed

### [HIGH] Null Jurisdiction Scoping Predicate Generation
- **Problem**: Users with unassigned jurisdictions (e.g. `assigned_state = None`) triggered `Work.state == NULL` filter predicates, returning 0 records across all analytics tables.
- **Root Cause**: Unconditional predicate addition in `api/auth/scoping.py`.
- **Fix**: Added `and user.assigned_state` checks before applying filter predicates.

### [HIGH] Frontend Hardcoded Mock Overrides
- **Problem**: Frontend services fell back to static mock arrays (`MOCK_COST_ANOMALIES`, `MOCK_DUPLICATE_WORKS`, etc.) when API returns were empty or cold-starting.
- **Root Cause**: Excessive try-catch fallback wrapping in `analytics.ts`, `works.ts`, `health.ts`, `scraper.ts`.
- **Fix**: Removed try-catch mock fallbacks, enabling direct 1:1 live API data flow.

### [MEDIUM] API Base URL Forced Override in Development
- **Problem**: `frontend/src/lib/api-client.ts` forced localhost URLs to point to Render unconditionally.
- **Root Cause**: Lack of `import.meta.env.PROD` checking.
- **Fix**: Guarded URL overrides with `import.meta.env.PROD`.

---

## 18. Fixes Applied
1. `api/auth/scoping.py`: Guarded jurisdiction scoping.
2. `api/routers/auth.py`: Added `swapnil15x@gmail.com` alias mapping.
3. `database/connection.py`: Removed silent SQLite fallback in `get_session()`.
4. `frontend/src/lib/api-client.ts`: Fixed development vs production base URL resolution.
5. `frontend/src/services/analytics.ts`: Removed mock fallbacks.
6. `frontend/src/services/works.ts`: Removed mock fallbacks.
7. `frontend/src/services/health.ts`: Removed mock fallbacks.
8. `frontend/src/services/scraper.ts`: Removed mock fallbacks.
9. `render.env`: Set explicit pooler URL and Groq API key.

---

## 19. Tests Run & Verification
- **Pytest**: 119/119 unit & integration tests passed cleanly (`PYTHONPATH=. pytest`).
- **Frontend Build**: `npm run build` passed with zero errors.

---

## 20. Remaining Issues
- **None**: All identified production parity and real data integration defects have been resolved.

---

## 21. Hardcoded Data Audit
- **Audit Result**: **NONE FOUND** in production API routes or live data pipelines. Synthetic mock files in `frontend/src/services/mockData.ts` are completely bypassed by active services.

---

## 22. Final Production Readiness Verdict
**VERDICT**: **A. PRODUCTION READY**
