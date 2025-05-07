"""Define the tournament."""

from typing import List
from models.player import Player


class Tournament:
    def __init__(
            self,
            name: str,
            location: str,
            start_date: str,
            end_date: str,
            number_of_rounds: int = 4,
            description: str = ""
    ):
        self.name: str = name
        self.location: str = location
        self.start_date: str = start_date  # Format: "YYYY-MM-DD"
        self.end_date: str = end_date  # Format: "YYYY-MM-DD"
        self.number_of_rounds: int = number_of_rounds
        # Numéro correspondant au tour actuel
        self.current_round: int = 0
        # Liste des joueurs enregistrés
        self.players: List[Player] = []
        # Liste des tours, chaque tour est une liste de matchs
        self.rounds: List[List[tuple]] = []
        self.description: str = description

    def add_player(self, player: Player):
        self.players.append(player)

    def __str__(self) -> str:
        return (f"Tournoi : {self.name} \n"
                f"Lieu : {self.location} \n"
                f"Dates : {self.start_date} -> {self.end_date} \n"
                f"Nombre de tours : {self.number_of_rounds} \n"
                f"Tour actuel : {self.current_round} \n"
                f"Description : {self.description} \n"
                f"Joueurs : {[str(player) for player in self.players]}")
