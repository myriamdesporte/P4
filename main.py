"""Entry point."""

from models.player import Player


def main():
    player1 = Player("Doe", "Joe", "2000-01-01", "AB12345")
    player2 = Player("Dupont", "Jean", "2000-02_01", "CD67890")

    print(player1)
    print(player2)

    players = [player1, player2]

    Player.save_players(players)

    for player in Player.load_players():
        print(player)


if __name__ == "__main__":
    main()
