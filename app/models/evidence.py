from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from app.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)

    trace_id = Column(String(100), nullable=False, index=True)

    evidence_type = Column(String(100), nullable=False)
    source = Column(String(100), nullable=False)

    data = Column(JSON, nullable=False, default=dict)

    integrity_hash = Column(String(64), nullable=False)

    collected_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    status = Column(String(30), nullable=False, default="COLLECTED")

    description = Column(Text, nullable=True)