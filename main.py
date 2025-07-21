"""Entry point."""
from domain.views.main_menu_view import MainMenuView
from infra.repositories.json_player_repository import JSONPlayerRepository
from infra.repositories.json_tournament_repository import JSONTournamentRepository


def main():
    # Repositories are instantiated here to allow easy replacement of the
    # persistence layer in the future (e.g. switch from JSON to SQLite)

    MainMenuView(
        player_repository=JSONPlayerRepository(),
        tournament_repository=JSONTournamentRepository()
    ).run()


if __name__ == "__main__":
    main()
