from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]


class AlertCreate(BaseModel):
    event_id: str
    source: str

    source_ip: IPv4Address | IPv6Address
    destination_ip: IPv4Address | IPv6Address

    destination_port: int | None = Field(
        default=None,
        ge=1,
        le=65535,
    )

    protocol: str
    alert_type: str

    mitre_technique: str | None = None

    severity: Severity
    timestamp: datetime