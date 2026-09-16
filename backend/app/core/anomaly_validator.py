from typing import Dict, Any, List

def validate_anomaly_thresholds(anomaly_scores: List[float], max_score_threshold: float = 100.0) -> Dict[str, Any]:
    """
    Validates expenditure anomaly detection output scores.
    Checks score range bounds [0.0, max_score_threshold] and flags high variance anomalies.
    """
    if not anomaly_scores:
        return {
            "valid_scores": True,
            "mean_score": 0.0,
            "anomalies_detected": 0,
            "critical_anomalies": 0
        }

    out_of_bounds = [s for s in anomaly_scores if s < 0.0 or s > max_score_threshold]
    if out_of_bounds:
        raise ValueError(f"Anomaly scores contain out-of-bounds values: {out_of_bounds}")

    mean_score = sum(anomaly_scores) / len(anomaly_scores)
    critical = [s for s in anomaly_scores if s >= 75.0]

    return {
        "valid_scores": True,
        "mean_score": float(mean_score),
        "anomalies_detected": len([s for s in anomaly_scores if s >= 50.0]),
        "critical_anomalies": len(critical)
    }
