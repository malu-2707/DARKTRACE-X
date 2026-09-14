 ValueError(
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
