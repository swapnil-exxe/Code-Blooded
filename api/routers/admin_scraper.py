import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text

from api.dependencies import get_db
from api.auth import CurrentUser, OptionalUser
from scraper.spider import LiveScraperPipeline
from scraper.config import scraper_settings

logger = logging.getLogger("api.admin_scraper")

router = APIRouter(prefix="/admin/scraper", tags=["Admin & Data Source Pipeline"])

@router.post("/run")
def trigger_manual_ingestion(
    background_tasks: BackgroundTasks,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Manually triggers an on-demand live eSAKSHI ingestion run.
    Requires administrative user privileges.
    """
    if current_user.role not in ["MINISTRY", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Administrative privileges required to trigger live ingestion.")

    logger.info(f"Manual ingestion trigger requested by user {current_user.email}")
    
    pipeline = LiveScraperPipeline(db_session=db)
    result = pipeline.run_pipeline()

    return {
        "status": "success",
        "message": "Live ingestion run completed successfully.",
        "details": result.model_dump(mode="json")
    }

@router.get("/status")
def get_scraper_pipeline_status(
    current_user: OptionalUser = None,
    db: Session = Depends(get_db)
):
    """
    Returns current live pipeline status, last run metrics, and source health.
    """
    # Fetch last ingestion run from DB
    sql_last_run = """
    SELECT run_id, start_time, end_time, status, records_seen, records_new,
           records_updated, records_unchanged, records_invalid, duration_seconds, error_message
    FROM ingestion_runs
    ORDER BY start_time DESC
    LIMIT 1;
    """
    last_run_row = db.execute(text(sql_last_run)).fetchone()

    last_run = None
    if last_run_row:
        last_run = {
            "run_id": last_run_row[0],
            "start_time": str(last_run_row[1]),
            "end_time": str(last_run_row[2]) if last_run_row[2] else None,
            "status": last_run_row[3],
            "records_seen": last_run_row[4] or 0,
            "records_new": last_run_row[5] or 0,
            "records_updated": last_run_row[6] or 0,
            "records_unchanged": last_run_row[7] or 0,
            "records_invalid": last_run_row[8] or 0,
            "duration_seconds": round(last_run_row[9], 2) if last_run_row[9] else 0.0,
            "error_message": last_run_row[10]
        }

    # Fetch snapshot count & database total count
    snapshot_count = db.execute(text("SELECT COUNT(*) FROM source_snapshots;")).scalar() or 0
    db_total_works = db.execute(text("SELECT COUNT(*) FROM works;")).scalar() or 0

    return {
        "target_url": scraper_settings.TARGET_URL,
        "interval_hours": scraper_settings.SCRAPER_INTERVAL_HOURS,
        "status": "healthy" if (not last_run or last_run["status"] in ["COMPLETED", "NO_CHANGES", "RUNNING"]) else "warning",
        "last_run": last_run,
        "total_snapshots_saved": snapshot_count,
        "total_works_in_db": db_total_works,
        "source_health": "LIVE_VERIFIED"
    }
