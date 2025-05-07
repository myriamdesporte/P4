"""Define the players."""

class Player:
    def __init__(self, last_name, first_name, birth_date, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date  # Format: "YYYY-MM-DD"
        self.national_id = national_id  # Ex: "AB12345"
        self.score = 0.0

    def __str__(self) -> str:
        return (f"{self.first_name} {self.last_name} ({self.national_id}) - "
                f"Né le {self.birth_date} - "
                f"Score : {self.score}")


