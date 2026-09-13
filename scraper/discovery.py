import logging
from typing import List, Dict, Any, Tuple, Optional
from scraper.client import ResilientScraperClient
from scraper.config import scraper_settings
from scraper.snapshots import SnapshotManager
from scraper.parsers.dashboard import DashboardParser
from scraper.parsers.works import WorksParser

logger = logging.getLogger("scraper.discovery")

class EndpointDiscovery:
    """
    Discovers and fetches public eSAKSHI dashboard data and REST endpoints
    without attempting private/authenticated access.
    """

    def __init__(self, client: Optional[ResilientScraperClient] = None):
        self.client = client or ResilientScraperClient()

    def discover_and_harvest(self) -> Tuple[List[Dict[str, Any]], str, int]:
        """
        Executes discovery workflow:
        1. Harvests live HTML from target dashboard.html
        2. Queries public REST tiles endpoint `/rest/PreLoginDashboardData/getTilesReportData`
        3. Returns combined raw extracted work rows, snapshot path, and status code.
        """
        target_url = scraper_settings.TARGET_URL
        logger.info(f"Initiating endpoint discovery for {target_url}")

        # Step 1: Harvest main HTML page
        html_res = self.client.fetch_url(target_url)
        status_code = html_res.get("status_code", 500)
        html_content = html_res.get("content", "")

        # Save HTML snapshot
        SnapshotManager.create_snapshot(target_url, html_content, status_code)

        raw_rows = []

        # Step 2: Query public REST endpoint
        rest_url = f"{scraper_settings.BASE_DOMAIN}/rest/PreLoginDashboardData/getTilesReportData"
        # Test Lok Sabha & Rajya Sabha public params
        payloads = [
            {"house": "LOK", "tenure": "18"},
            {"house": "RAJYA", "tenure": "0"}
        ]

        for p in payloads:
            rest_res = self.client.fetch_post_json(rest_url, p)
            if rest_res.get("status_code") == 200 and rest_res.get("data"):
                # Save REST JSON snapshot
                SnapshotManager.create_snapshot(rest_url, rest_res["data"], 200)
                parsed = DashboardParser.parse_tile_report_json(rest_res["data"])
                raw_rows.extend(parsed)

        logger.info(f"Discovery completed. Harvested {len(raw_rows)} raw records.")
        return raw_rows, target_url, status_code
