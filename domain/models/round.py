"""Define a round in a chess tournament."""

from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from domain.models.match import Match


class Round:
    def __init__(
        self,
        name: str,
        matches: Optional[List[Match]] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        round_id: Optional[str] = None,
    ):
        """Initialize a Round instance with optional match list and timestamps."""
        self.name = name
        self.matches: List[Match] = matches if matches else []
        self.start_datetime: Optional[datetime] = start_datetime
        self.end_datetime: Optional[datetime] = end_datetime
        self.round_id = round_id

    def start(self):
        """Set the start time of the round to the current time."""
        self.start_datetime = datetime.now()

    def end(self):
        """Set the end time of the round to the current time."""
        self.end_datetime = datetime.now()

    def to_dict(self) -> dict:
        """Convert the round instance into a dictionary."""
        return {
            "name": self.name,
            "matches": [
                match.to_dict() for match in self.matches
            ],
            "start_datetime": self.start_datetime.isoformat() if self.start_datetime else None,
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
            "round_id": self.round_id,
        }

    @classmethod
    def from_dict(cls, round_data: dict) -> Round:
        matches = [Match.from_dict(m) for m in round_data.get("matches", [])]

        start_dt = round_data.get("start_datetime")
        start_datetime = datetime.fromisoformat(start_dt) if isinstance(start_dt, str) else None

        end_dt = round_data.get("end_datetime")
        end_datetime = datetime.fromisoformat(end_dt) if isinstance(end_dt, str) else None

        return cls(
            name=round_data["name"],
            matches=matches,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            round_id=round_data.get("round_id"),
        )
