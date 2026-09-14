import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

import urllib.parse

def _sanitize_db_url(raw_url: str) -> str:
    if not raw_url or "sqlite" in raw_url:
        return raw_url
    raw_url = raw_url.replace("postgres://", "postgresql://").replace("?pgbouncer=true", "")
    if "://" not in raw_url or "@" not in raw_url:
        return raw_url

    try:
        scheme, remainder = raw_url.split("://", 1)
        user_pass, host_port_db = remainder.rsplit("@", 1)

        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
        else:
            user, password = user_pass, ""

        unquoted_pass = urllib.parse.unquote(password)
        quoted_pass = urllib.parse.quote(unquoted_pass, safe="")

        if "db.fcpwrmzviqrhsdgelwmk.supabase.co" in host_port_db or "aws-0-ap-south-1.pooler.supabase.com" in host_port_db:
            host_port_db = "aws-0-ap-south-1.pooler.supabase.com:6543/" + host_port_db.split("/", 1)[-1]
            if user == "postgres":
                user = "postgres.fcpwrmzviqrhsdgelwmk"

        return f"{scheme}://{user}:{quoted_pass}@{host_port_db}"
    except Exception:
        return raw_url

def get_db_url() -> str:
    """Retrieves Database URL from environment or constructs from parts, falling back to live Supabase PostgreSQL."""
    sqlite_path = Path(__file__).resolve().parent.parent / "database" / "mplads_master.db"
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure_sqlite_ready(path: Path):
        if not path.exists() or path.stat().st_size < 1000000:
            import threading
            print("[DATABASE] SQLite database missing or empty. Starting background auto-population...")
            def _bg_populate():
                try:
                    from database.populate_sqlite import populate_database
                    populate_database()
                except Exception as e:
                    print(f"[DATABASE WARN] Auto-population of SQLite database failed: {e}")
            t = threading.Thread(target=_bg_populate, daemon=True)
            t.start()

    # 1. Check direct URL or DATABASE_URL from environment (Supabase PostgreSQL)
    direct = os.getenv("DIRECT_URL")
    if direct and "[YOUR-PASSWORD]" not in direct and "YOUR_PASSWORD" not in direct:
        return _sanitize_db_url(direct)

    url = os.getenv("DATABASE_URL")
    if url and "[YOUR-PASSWORD]" not in url and "YOUR_PASSWORD" not in url:
        return _sanitize_db_url(url)

    # 2. Check individual Postgres environment components
    password = os.getenv("DB_PASSWORD", "")
    if password and password not in ["", "YOUR_PASSWORD", "[YOUR-PASSWORD]"]:
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        db = os.getenv("DB_NAME", "postgres")
        user = os.getenv("DB_USER", "postgres")
        raw_pg = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        return _sanitize_db_url(raw_pg)

    raise ValueError("DATABASE_URL environment variable is not configured. Please set DATABASE_URL in your .env file.")

def get_engine(db_url: str = None, pool_size: int = 10, max_overflow: int = 20):
    """Creates a thread-safe SQLAlchemy engine with connection pooling."""
    if db_url is None:
        db_url = get_db_url()
    
    if db_url.startswith("sqlite"):
        return create_engine(
            db_url,
            connect_args={"check_same_thread": False},
        )

    connect_args = {
        "connect_timeout": 15,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
    
    return create_engine(
        db_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,
        connect_args=connect_args,
    )

_engine = None
_SessionLocal = None

def get_session():
    """Contextual session generator using canonical database engine."""
    global _engine, _SessionLocal
    if _engine is None:
        _engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _SessionLocal()

def check_connection() -> bool:
    """Verifies that the database is reachable."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            from sqlalchemy import text
            res = conn.execute(text("SELECT 1;")).scalar()
            return res == 1
    except Exception:
        return False
