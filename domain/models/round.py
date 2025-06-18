"""Define a round in a chess tournament."""
from typing import List, Optional
from datetime import datetime
from domain.models.match import Match


class Round:
    def __init__(
        self,
        name: str,
        matches: List[Match] | None = None,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        round_id: Optional[str] = None,
    ):
        self.name = name
        self.matches: List[Match] = matches if matches else []
        self.start_datetime: datetime = start_datetime or datetime.now()
        self.end_datetime: datetime | None = end_datetime
        self.round_id = round_id

    def add_match(self, match: Match):
        """Add a match to this round."""
        self.matches.append(match)

    def start(self):
        """Mark the round as started (actualize start time)."""
        self.start_datetime = datetime.now()

    def end(self):
        """Mark the round as finished and set time."""
        self.end_datetime = datetime.now()

    def is_finished(self) -> bool:
        """Return True if the round is finished."""
        return self.end_datetime is not None

    def to_dict(self) -> dict:
        """Convert the round instance into a dictionary."""
        return {
            "name": self.name,
            "matches": [
                match.data for match in self.matches
            ],
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime" : self.end_datetime.isoformat() if self.end_datetime else None,
            "round_id": self.round_id
        }

    @classmethod
    def from_dict(cls, round_data: dict):
        """Create a Round instance from a dictionary (e.g. loaded from JSON)."""
        round_instance = cls(round_data["name"])
        round_instance.start_datetime = datetime.fromisoformat(round_data["start_datetime"])
        end_datetime = round_data.get("end_datetime")
        round_instance.end_datetime = datetime.fromisoformat(end_datetime) if end_datetime else None
        round_instance.round_id = round_data.get("round_id")

        for match_data in round_data.get("matches", []):
            round_instance.matches.append(match_data)

        return round_instance
