"""Entry point."""
from models.player import Player


def main():
    player = Player("Doe", "Joe", "2000-01-01", "AB12345")

    print(player)


if __name__ == "__main__":
    main()
