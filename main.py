"""Entry point."""

from domain.views.player_view import PlayerView
from domain.views.tournament_view import TournamentView


def main():
    # Vue gestionnaire de joueurs
    #view = PlayerView()
    #view.display_menu()

    # Vue gestionnaire de tournois
    view = TournamentView()
    view.display_menu()


if __name__ == "__main__":
    main()
