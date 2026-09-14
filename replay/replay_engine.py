from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator


class ReplayEngine:
    """Replay SOC telemetry events from a JSON scenario file."""

    def __init__(self, scenario_path: str | Path):
        self.scenario_path = Path(scenario_path)

    def load(self) -> Any:
        """Load the scenario JSON file."""
        if not self.scenario_path.exists():
            raise FileNotFoundError(
                f"Scenario file not found: {self.scenario_path}"
            )

        with self.scenario_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def events(self) -> Iterator[dict[str, Any]]:
        """Yield events from list or object-based JSON scenarios."""
        scenario = self.load()

        if isinstance(scenario, list):
            events = scenario
        elif isinstance(scenario, dict):
            events = scenario.get("events", [])
        else:
            raise ValueError(
                "Invalid scenario format: expected a JSON list or object"
            )

        for event in events:
            if not isinstance(event, dict):
                raise ValueError("Each replay event must be a JSON object")

            yield event

    def replay(self) -> list[dict[str, Any]]:
        """Replay all events and return them as a list."""
        return list(self.events())


if __name__ == "__main__":
    scenario = Path(__file__).parent.parent / "telemetry" / "demo_events.json"

    engine = ReplayEngine(scenario)

    events = engine.replay()

    print(f"Replayed events: {len(events)}")

    for event in events:
        event_type = event.get("attack_type", event.get("event_type", "UNKNOWN"))
        print(
            f"{event['event_id']} | "
            f"{event.get('source', 'UNKNOWN')} | "
            f"{event_type} | "
            f"{event.get('severity', 'UNKNOWN')}"
        )
