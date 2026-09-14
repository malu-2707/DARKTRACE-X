from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(String, default="low")
    is_active = Column(Boolean, default=True)