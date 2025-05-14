"""Entry point."""

from views.player_view import PlayerView


def main():
    view = PlayerView()
    view.display_menu()


if __name__ == "__main__":
    main()
