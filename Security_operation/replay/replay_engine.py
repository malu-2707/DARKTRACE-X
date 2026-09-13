cat > replay/replay_engine.py <<'PY'
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator


class ReplayEngine:
    """Replays predefined SOC event scenarios."""

    def __init__(self, scenario_path: str | Path):
        self.scenario_path = Path(scenario_path)

    def load(self) -> dict[str, Any]:
        with self.scenario_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def events(self) -> Iterator[dict[str, Any]]:
        scenario = self.load()
        events = scenario.get("events", [])

        for event in events:
            yield event

    def replay(self) -> list[dict[str, Any]]:
        return list(self.events())


if __name__ == "__main__":
    scenario = Path(__file__).parent / "scenarios" / "ssh_failed.json"

    engine = ReplayEngine(scenario)

    for event in engine.replay():
        print(json.dumps(event, indent=2))
PY
