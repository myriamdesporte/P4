"""Define the tournament controller."""
from domain.models.tournament import Tournament
from domain.ports.player_repository import IPlayerRepository
from domain.ports.tournament_repository import ITournamentRepository
from infra.utils.tournament_utils import tournament_with_loaded_players


class TournamentController:
    def __init__(
            self,
            tournament_repository: ITournamentRepository,
            player_repository: IPlayerRepository
    ):
        """
        Initialize the controller by setting the repository.
        """
        self.tournament_repository = tournament_repository
        self.player_repository = player_repository

    def create_tournament(
            self,
            name: str,
            location: str,
            start_date: str,
            end_date: str,
            number_of_rounds: int = 4,
            description: str = ""
    ) -> Tournament:
        """
        Create a new tournament, add to the list, and save all tournaments.

        Args:
            name (str): Tournament name.
            location (str): Tournament location.
            start_date (str): Tournament start date.
            end_date (str): Tournament end date.
            number_of_rounds (int): Total number of rounds (default: 4).
            description (str): Optional description of the tournament.

        Returns:
            Tournament: The newly created Tournament instance.
        """
        tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            description=description
        )
        tournaments = self.tournament_repository.load_tournaments()
        tournaments.append(tournament)
        self.tournament_repository.save_tournaments(tournaments)
        return tournament

    def list_tournaments(self):
        """
        Retrieve all tournaments from the repository with loaded players.

        Returns:
            List[Tournament]: A list of all saved tournaments.
        """
        tournaments = self.tournament_repository.load_tournaments()
        return [
            tournament_with_loaded_players(
                tournament,
                self.player_repository
            )
            for tournament in tournaments
        ]
