"""Entry point."""
from domain.views.main_menu_view import MainMenuView


def main():
    MainMenuView().display_menu()


if __name__ == "__main__":
    main()
