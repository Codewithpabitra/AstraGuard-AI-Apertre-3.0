"""High-resolution latency tracking for HIL validation."""

import time
import csv
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class LatencyMeasurement:
    """Single latency measurement point."""

    timestamp: float  # Unix timestamp
    metric_type: str  # fault_detection, agent_decision, recovery_action
    satellite_id: str  # SAT1, SAT2, etc.
    duration_ms: float  # Measured latency in milliseconds
    scenario_time_s: float  # Simulation time when measured


class LatencyCollector:
    """Captures high-resolution timing data across swarm (10Hz cadence)."""

    def __init__(self):
        """Initialize collector with empty measurements."""
        self.measurements: List[LatencyMeasurement] = []
        self._start_time = time.time()
        self._measurement_log: Dict[str, int] = defaultdict(int)

    def record_fault_detection(
        self, sat_id: str, scenario_time_s: float, detection_delay_ms: float
    ) -> None:
        """
        Record fault detection latency.

        Args:
            sat_id: Satellite identifier (e.g., "SAT1")
            scenario_time_s: Simulation time when detected
            detection_delay_ms: Time from fault injection to detection
        """
        if not sat_id or not isinstance(sat_id, str):
            logger.warning(f"Invalid sat_id: {sat_id}")
            return
        
        if not isinstance(scenario_time_s, (int, float)) or scenario_time_s < 0:
            logger.warning(f"Invalid scenario_time_s: {scenario_time_s}")
            return
        
        if not isinstance(detection_delay_ms, (int, float)) or detection_delay_ms < 0:
            logger.warning(f"Invalid detection_delay_ms: {detection_delay_ms}")
            return

        try:
            measurement = LatencyMeasurement(
                timestamp=time.time(),
                metric_type="fault_detection",
                satellite_id=sat_id,
                duration_ms=float(detection_delay_ms),
                scenario_time_s=float(scenario_time_s),
            )
            self.measurements.append(measurement)
            self._measurement_log["fault_detection"] += 1
            logger.debug(f"Recorded fault detection latency: {sat_id}, {detection_delay_ms}ms")
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to create fault detection measurement: {e}")
        except Exception as e:
            logger.error(f"Unexpected error recording fault detection: {e}")

    def record_agent_decision(
        self, sat_id: str, scenario_time_s: float, decision_time_ms: float
    ) -> None:
        """
        Record agent decision latency.

        Args:
            sat_id: Satellite identifier
            scenario_time_s: Simulation time of decision
            decision_time_ms: Time for agent to process and decide
        """
        if not sat_id or not isinstance(sat_id, str):
            logger.warning(f"Invalid sat_id: {sat_id}")
            return
        
        if not isinstance(scenario_time_s, (int, float)) or scenario_time_s < 0:
            logger.warning(f"Invalid scenario_time_s: {scenario_time_s}")
            return
        
        if not isinstance(decision_time_ms, (int, float)) or decision_time_ms < 0:
            logger.warning(f"Invalid decision_time_ms: {decision_time_ms}")
            return

        try:
            measurement = LatencyMeasurement(
                timestamp=time.time(),
                metric_type="agent_decision",
                satellite_id=sat_id,
                duration_ms=float(decision_time_ms),
                scenario_time_s=float(scenario_time_s),
            )
            self.measurements.append(measurement)
            self._measurement_log["agent_decision"] += 1
            logger.debug(f"Recorded agent decision latency: {sat_id}, {decision_time_ms}ms")
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to create agent decision measurement: {e}")
        except Exception as e:
            logger.error(f"Unexpected error recording agent decision: {e}")

    def record_recovery_action(
        self, sat_id: str, scenario_time_s: float, action_time_ms: float
    ) -> None:
        """
        Record recovery action execution latency.

        Args:
            sat_id: Satellite identifier
            scenario_time_s: Simulation time of action
            action_time_ms: Time to execute recovery action
        """
        if not sat_id or not isinstance(sat_id, str):
            logger.warning(f"Invalid sat_id: {sat_id}")
            return
        
        if not isinstance(scenario_time_s, (int, float)) or scenario_time_s < 0:
            logger.warning(f"Invalid scenario_time_s: {scenario_time_s}")
            return
        
        if not isinstance(action_time_ms, (int, float)) or action_time_ms < 0:
            logger.warning(f"Invalid action_time_ms: {action_time_ms}")
            return

        try:
            measurement = LatencyMeasurement(
                timestamp=time.time(),
                metric_type="recovery_action",
                satellite_id=sat_id,
                duration_ms=float(action_time_ms),
                scenario_time_s=float(scenario_time_s),
            )
            self.measurements.append(measurement)
            self._measurement_log["recovery_action"] += 1
            logger.debug(f"Recorded recovery action latency: {sat_id}, {action_time_ms}ms")
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to create recovery action measurement: {e}")
        except Exception as e:
            logger.error(f"Unexpected error recording recovery action: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Calculate aggregate latency statistics.

        Returns:
            Dict with per-metric-type statistics (count, mean, p50, p95, max)
        """
        if not self.measurements:
            logger.info("No measurements available for statistics")
            return {}

        try:
            by_type = defaultdict(list)
            for m in self.measurements:
                by_type[m.metric_type].append(m.duration_ms)

            stats = {}
            for metric_type, latencies in by_type.items():
                if not latencies:
                    continue
                    
                try:
                    sorted_latencies = sorted(latencies)
                    count = len(sorted_latencies)

                    stats[metric_type] = {
                        "count": count,
                        "mean_ms": sum(latencies) / count if count > 0 else 0,
                        "p50_ms": sorted_latencies[count // 2] if count > 0 else 0,
                        "p95_ms": sorted_latencies[int(count * 0.95)] if count > 0 else 0,
                        "p99_ms": sorted_latencies[int(count * 0.99)] if count > 0 else 0,
                        "max_ms": max(latencies) if latencies else 0,
                        "min_ms": min(latencies) if latencies else 0,
                    }
                except (TypeError, ValueError, ZeroDivisionError) as e:
                    logger.warning(f"Failed to calculate stats for {metric_type}: {e}")
                    continue

            logger.debug(f"Calculated statistics for {len(stats)} metric types")
            return stats
            
        except Exception as e:
            logger.error(f"Unexpected error calculating statistics: {e}")
            return {}

    def get_stats_by_satellite(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate statistics per satellite.

        Returns:
            Dict mapping satellite ID to stats
        """
        if not self.measurements:
            logger.info("No measurements available for satellite statistics")
            return {}

        try:
            by_satellite = defaultdict(lambda: defaultdict(list))

            for m in self.measurements:
                by_satellite[m.satellite_id][m.metric_type].append(m.duration_ms)

            stats = {}
            for sat_id, metrics in by_satellite.items():
                stats[sat_id] = {}
                for metric_type, latencies in metrics.items():
                    if not latencies:
                        continue
                        
                    try:
                        sorted_latencies = sorted(latencies)
                        count = len(sorted_latencies)

                        stats[sat_id][metric_type] = {
                            "count": count,
                            "mean_ms": sum(latencies) / count if count > 0 else 0,
                            "p50_ms": sorted_latencies[count // 2] if count > 0 else 0,
                            "p95_ms": sorted_latencies[int(count * 0.95)] if count > 0 else 0,
                            "max_ms": max(latencies) if latencies else 0,
                        }
                    except (TypeError, ValueError, ZeroDivisionError) as e:
                        logger.warning(f"Failed to calculate stats for {sat_id}/{metric_type}: {e}")
                        continue

            logger.debug(f"Calculated statistics for {len(stats)} satellites")
            return stats
            
        except Exception as e:
            logger.error(f"Unexpected error calculating satellite statistics: {e}")
            return {}

    def export_csv(self, filename: str) -> None:
        """
        Export raw measurements to CSV.

        Args:
            filename: Path to output CSV file
        """
        if not filename or not isinstance(filename, str):
            logger.error(f"Invalid filename: {filename}")
            return
        
        if not self.measurements:
            logger.warning("No measurements to export")
            return

        try:
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w", newline="", encoding='utf-8') as f:
                fieldnames = [
                    "timestamp",
                    "metric_type",
                    "satellite_id",
                    "duration_ms",
                    "scenario_time_s",
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for m in self.measurements:
                    try:
                        writer.writerow(asdict(m))
                    except (TypeError, ValueError) as e:
                        logger.warning(f"Failed to write measurement row: {e}")
                        continue

            logger.info(f"Exported {len(self.measurements)} measurements to {filepath}")
            
        except (OSError, IOError, PermissionError) as e:
            logger.error(f"Failed to write CSV file {filename}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error exporting CSV: {e}")
            raise

    def get_summary(self) -> Dict[str, Any]:
        """
        Get human-readable summary.

        Returns:
            Dict with high-level metrics summary
        """
        if not self.measurements:
            return {"total_measurements": 0, "metrics": {}}

        return {
            "total_measurements": len(self.measurements),
            "measurement_types": dict(self._measurement_log),
            "stats": self.get_stats(),
            "stats_by_satellite": self.get_stats_by_satellite(),
        }

    def reset(self) -> None:
        """Clear all measurements."""
        self.measurements.clear()
        self._measurement_log.clear()

    def __len__(self) -> int:
        """Return number of measurements."""
        return len(self.measurements)
