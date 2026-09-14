import hashlib
import json
from typing import Any


def generate_integrity_hash(data: Any) -> str:
    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        default=str
    )

    return hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()