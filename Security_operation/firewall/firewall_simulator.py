
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FirewallRule:
    source_ip: str | None = None
    destination_ip: str | None = None
    destination_port: int | None = None
    protocol: str | None = None
    action: str = "ALLOW"


class FirewallSimulator:
    """Simulates basic firewall rule evaluation."""

    def __init__(self, rules: list[FirewallRule] | None = None):
        self.rules = rules or []

    def add_rule(self, rule: FirewallRule) -> None:
        self.rules.append(rule)

    def evaluate(
        self,
        source_ip: str,
        destination_ip: str,
        destination_port: int,
        protocol: str,
    ) -> str:
        for rule in self.rules:
            if rule.source_ip is not None and rule.source_ip != source_ip:
                continue
            if rule.destination_ip is not None and rule.destination_ip != destination_ip:
                continue
            if rule.destination_port is not None and rule.destination_port != destination_port:
                continue
            if rule.protocol is not None and rule.protocol.upper() != protocol.upper():
                continue

            return rule.action.upper()

        return "ALLOW"


if __name__ == "__main__":
    firewall = FirewallSimulator()

    firewall.add_rule(
        FirewallRule(
            source_ip="192.168.56.20",
            destination_ip="192.168.56.10",
            destination_port=22,
            protocol="TCP",
            action="BLOCK",
        )
    )

    result = firewall.evaluate(
        source_ip="192.168.56.20",
        destination_ip="192.168.56.10",
        destination_port=22,
        protocol="TCP",
    )

    print(f"Firewall decision: {result}")
