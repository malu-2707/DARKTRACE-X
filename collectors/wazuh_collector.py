from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

from normalizer.schema import EventType, Severity, SOCAlert


def map_severity(level: int) -> Severity:
    """Map Wazuh rule level to SOC severity."""
    if level >= 12:
        return Severity.CRITICAL
    if level >= 8:
        return Severity.HIGH
    if level >= 4:
        return Severity.MEDIUM
    return Severity.LOW


def detect_event_type(alert: dict[str, Any]) -> EventType:
    """Determine the normalized event type from a Wazuh alert."""

    rule = alert.get("rule", {})
    groups = [str(group).lower() for group in rule.get("groups", [])]
    data = alert.get("data", {})

    if any(
        keyword in " ".join(groups)
        for keyword in ("auth", "authentication", "sshd", "pam")
    ):
        return EventType.AUTHENTICATION

    if any(
        key in data
        for key in ("srcip", "src_ip", "dstip", "dst_ip", "srcport", "dstport")
    ):
        return EventType.NETWORK_ALERT

    if any(
        keyword in " ".join(groups)
        for keyword in ("process", "syscheck", "rootcheck")
    ):
        return EventType.PROCESS_ACTIVITY

    return EventType.SERVER_LOG


def get_value(data: dict[str, Any], *keys: str) -> Any:
    """Return the first available value from a dictionary."""
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def normalize_wazuh_alert(alert: dict[str, Any]) -> SOCAlert:
    """Convert one raw Wazuh alert into the project's SOCAlert model."""

    rule = alert.get("rule", {})
    agent = alert.get("agent", {})
    data = alert.get("data", {})

    level = int(rule.get("level", 0))

    source_ip = get_value(data, "srcip", "src_ip", "source_ip")
    destination_ip = get_value(data, "dstip", "dst_ip", "destination_ip")

    source_port = get_value(data, "srcport", "src_port", "source_port")
    destination_port = get_value(
        data, "dstport", "dst_port", "destination_port"
    )

    username = get_value(
        data,
        "dstuser",
        "srcuser",
        "user",
        "username",
    )

    mitre = rule.get("mitre", {})
    mitre_id = None

    if isinstance(mitre, dict):
        mitre_id = get_value(mitre, "id", "technique")

    attack_type = (
        rule.get("groups", [None])[0]
        if rule.get("groups")
        else "WAZUH_ALERT"
    )

    metadata = {
        "wazuh_rule_id": rule.get("id"),
        "wazuh_rule_level": level,
        "wazuh_rule_description": rule.get("description"),
        "wazuh_groups": rule.get("groups", []),
        "wazuh_agent_id": agent.get("id"),
        "wazuh_agent_name": agent.get("name"),
        "wazuh_manager": alert.get("manager", {}).get("name"),
        "wazuh_location": alert.get("location"),
        "wazuh_decoder": alert.get("decoder", {}),
    }

    return SOCAlert(
        event_id=str(alert.get("id", "")),
        timestamp=alert["timestamp"],
        source="wazuh",
        event_type=detect_event_type(alert),
        severity=map_severity(level),
        source_ip=source_ip,
        destination_ip=destination_ip,
        source_port=int(source_port) if source_port else None,
        destination_port=int(destination_port) if destination_port else None,
        protocol=get_value(data, "protocol"),
        attack_type=str(attack_type),
        mitre_technique=mitre_id,
        hostname=agent.get("name"),
        username=username,
        message=rule.get("description") or alert.get("full_log"),
        metadata=metadata,
    )


def read_wazuh_alerts(
    alert_file: str | Path,
    limit: int | None = None,
) -> Iterator[SOCAlert]:
    """Read JSON-line Wazuh alerts and yield normalized SOC alerts."""

    path = Path(alert_file)

    if not path.exists():
        raise FileNotFoundError(f"Wazuh alert file not found: {path}")

    count = 0

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                alert = json.loads(line)
                yield normalize_wazuh_alert(alert)
                count += 1
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue

            if limit is not None and count >= limit:
                break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Read and normalize Wazuh alerts."
    )
    parser.add_argument(
        "--file",
        default="/var/ossec/logs/alerts/alerts.json",
        help="Path to Wazuh alerts.json",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of alerts to read",
    )

    args = parser.parse_args()

    for alert in read_wazuh_alerts(args.file, args.limit):
        print(alert.model_dump_json())
