import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def get_db_url() -> str:
    """Retrieves Database URL from environment or constructs from parts, falling back to local SQLite if configured or unavailable."""
    sqlite_path = Path(__file__).resolve().parent.parent / "database" / "mplads_master.db"
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure_sqlite_ready(path: Path):
        if not path.exists() or path.stat().st_size < 1000000:
            try:
                print("[DATABASE] SQLite database missing or empty. Auto-populating full dataset...")
                from database.populate_sqlite import populate_database
                populate_database()
            except Exception as e:
                print(f"[DATABASE WARN] Auto-population of SQLite database failed: {e}")

    if os.getenv("USE_LOCAL_SQLITE", "true").lower() in ["true", "1", "yes"]:
        _ensure_sqlite_ready(sqlite_path)
        return f"sqlite:///{sqlite_path}"

    direct = os.getenv("DIRECT_URL")
    if direct and "[YOUR-PASSWORD]" not in direct:
        return direct

    url = os.getenv("DATABASE_URL")
    if url and "[YOUR-PASSWORD]" not in url:
        return url.replace("?pgbouncer=true", "")

    # Fallback to individual components if valid
    password = os.getenv("DB_PASSWORD", "")
    if password and password not in ["", "YOUR_PASSWORD", "[YOUR-PASSWORD]"]:
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        db = os.getenv("DB_NAME", "postgres")
        user = os.getenv("DB_USER", "postgres")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    # Fallback to local SQLite database
    sqlite_path = Path(__file__).resolve().parent.parent / "database" / "mplads_master.db"
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    _ensure_sqlite_ready(sqlite_path)
    return f"sqlite:///{sqlite_path}"

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
    """Contextual session generator."""
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
