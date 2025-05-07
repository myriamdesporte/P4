"""Entry point."""

from models.player import Player
from models.tournament import Tournament


def main():
    player1 = Player("Doe", "Joe", "2000-01-01", "AB12345")
    player2 = Player("Martin", "Jean", "2000-02-01", "CD67890")

    print(player1)

    tournament = Tournament("Tournoi", "Lyon", "2025-05-07", "2025-05-11", 4)
    tournament.add_player(player1)
    tournament.add_player(player2)

    print(tournament)


if __name__ == "__main__":
    main()
