from random import shuffle
from typing import List, Tuple
from domain.models.player import Player
from domain.models.tournament import Tournament
from domain.ports.player_repository import IPlayerRepository


def tournament_with_loaded_players(
        tournament: Tournament,
        player_repository: IPlayerRepository
) -> Tournament:
    """
    Return a new instance of Tournament with players loaded from their IDs,
    without modifying the existing instance of Tournament.
    """
    loaded_players: List[Player] = []
    for player_id in tournament.players:
        player = player_repository.get_by_id(player_id)
        if player:
            loaded_players.append(player)

    return Tournament(
        name=tournament.name,
        location=tournament.location,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
        number_of_rounds=tournament.number_of_rounds,
        current_round_number=tournament.current_round_number,
        status=tournament.status,
        rounds=tournament.rounds,
        players=loaded_players,
        scores=tournament.scores,
        description=tournament.description,
        tournament_id=tournament.tournament_id
    )


def have_played_before(
        player1: Player,
        player2: Player,
        tournament: Tournament
) -> bool:
    """
    Check whether two players have already played against each other in
    this tournament.
    """
    for round_instance in tournament.rounds:
        for match in round_instance.matches:
            p1, p2 = match.get_players()
            if {p1.national_chess_id, p2.national_chess_id} == {player1.national_chess_id, player2.national_chess_id}:
                return True
    return False


def create_pairs_for_next_round(
        tournament: Tournament
) -> List[Tuple[Player, Player]]:
    """
    Creates pairs for the next round of the tournament.
    Returns the list of pairs (Player1, Player2).
    """

    # Get all players in the tournament
    players: List[Player] = tournament.players.copy()

    # Sort players by descending score
    if tournament.current_round_number == 1:
        # First round: pair players randomly
        shuffle(players)
    else:
        # Other rounds: sort players by descending score
        players.sort(key=lambda p: p.score, reverse=True)

    pairs: List[Tuple[Player, Player]] = []
    paired: set[str] = set()  # Track already paired player IDs

    for i, player in enumerate(players):
        if player.national_chess_id in paired:
            continue

        # Search for an opponent who has not yet been paired nor played against.
        for opponent in players[i+1:]:
            if opponent.national_chess_id in paired:
                continue
            if not have_played_before(player, opponent, tournament):
                pairs.append((player, opponent))
                paired.add(player.national_chess_id)
                paired.add(opponent.national_chess_id)
                break
        else:
            # If no suitable new opponent found, pair with any available player
            for opponent in players[i+1:]:
                if opponent.national_chess_id not in paired:
                    pairs.append((player, opponent))
                    paired.add(player.national_chess_id)
                    paired.add(opponent.national_chess_id)
                    break

    return pairs
