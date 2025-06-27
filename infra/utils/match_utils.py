from random import randint
from domain.models.match import Match
from domain.ports.player_repository import IPlayerRepository


def match_with_loaded_players(
        match: Match,
        player_repository: IPlayerRepository
) -> Match:
    """
    Return a new instance of Match with players loaded from their IDs,
    without modifying the existing instance of Match.
    """
    p1, p1_score = match.data[0]
    p2, p2_score = match.data[1]

    return Match(
        player1=player_repository.get_by_id(p1),
        player2=player_repository.get_by_id(p2),
        player1_score=p1_score,
        player2_score=p2_score,
    )

def input_result(match: Match):
    while True:
        print(f"1 → Le gagnant est {match.data[0][0]}")
        print(f"2 → Le gagnant est {match.data[1][0]}")
        print(f"3 → Match nul")
        print(f"4 → Choix aléatoire")

        choice = input("Votre choix : ")

        if choice == "4":
            choice = str(randint(1, 3))

        if choice == "1":
            match.set_scores(1.0, 0.0)
            print(match)
            return
        elif choice == "2":
            match.set_scores(0.0, 1.0)
            print(match)
            return
        elif choice == "3":
            match.set_scores(0.5, 0.5)
            print(match)
            return
        else:
            print("Choix invalide. Réessayez.")
