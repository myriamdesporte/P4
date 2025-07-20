"""Handle user input with validation."""
from datetime import datetime

from rich.console import Console

from infra.utils.validators import (
    is_valid_name,
    is_valid_date,
    is_valid_national_chess_id,
    is_valid_tournament_id,
    is_valid_number
)


class InputView:
    def __init__(self, console: Console):
        """Initialize InputView with a Rich console instance."""
        self.console = console

    def input_name(
            self,
            name_type: str,
            add_on: str = "",
            allow_empty: bool = False
    ) -> str | None:
        """Prompt for a name and validate it. Allows empty input if updating."""
        while True:
            name = input(f"{name_type} {add_on}: ").strip()
            if allow_empty and name == "":
                return None
            if is_valid_name(name):
                return name
            self.console.print(f"[bold red]{name_type} invalide. Veuillez réessayer.[/bold red]")

    def input_date(
            self,
            date_type: str,
            allow_empty: bool = False
    ) -> str | None:
        """Prompt for a name and validate it. Allows empty input if updating."""
        while True:
            date = input(f"{date_type} (format JJ-MM-AAAA): ").strip()
            if allow_empty and date == "":
                return None
            if is_valid_date(date):
                return date
            self.console.print("[bold red]Format invalide. Utilisez JJ-MM-AAAA.[/bold red]")

    def input_start_date(self) -> str | None:
        """Prompt for a start date that must be today or later."""
        while True:
            start_date = self.input_date("Date de début: ")
            start_date_obj = datetime.strptime(start_date, "%d-%m-%Y").date()
            if start_date_obj < datetime.now().date():
                self.console.print("[red]La date de début ne peut pas être antérieure à aujourd'hui.[/red]")
                continue
            return start_date

    def input_end_date(self, start_date: str) -> str | None:
        """Prompt for an end date that must be after or equal to the start date."""
        start_date_obj = datetime.strptime(start_date, "%d-%m-%Y").date()
        while True:
            end_date = self.input_date("Date de fin: ")
            end_date_obj = datetime.strptime(end_date, "%d-%m-%Y").date()
            if end_date_obj < start_date_obj:
                self.console.print("[red]La date de fin ne peut pas être antérieure à la date de début.[/red]")
                continue
            return end_date

    def input_number_of_rounds(self) -> int:
        while True:
            number = input("Nombre de rounds (4 par défaut) : ")
            if number == "":
                return 4
            if is_valid_number(number):
                return int(number)
            self.console.print("[bold red]Nombre invalide. Entrez un entier entre 1 et 10.[/bold red]")

    def input_national_chess_id(self) -> str:
        """Prompt for an id and validate it."""
        while True:
            national_chess_id = input("Identifiant national d'échecs (ex: AB12345): ").strip()
            if is_valid_national_chess_id(national_chess_id):
                return national_chess_id
            self.console.print("[bold red]Identifiant invalide. Veuillez réessayer."
                               "Format attendu : 2 lettres suivies de 5 chiffres (ex: AB12345).[/bold red]")

    def input_tournament_id(self) -> str:
        """Prompt for a tournament id and validate it."""
        while True:
            tournament_id = input("ID du tournoi (ex: T001): ").strip()
            if is_valid_tournament_id(tournament_id):
                return tournament_id
            self.console.print("[bold red]Identifiant invalide. "
                               "Veuillez réessayer.[/bold red]")
