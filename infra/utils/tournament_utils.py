"""Tournament utilities for resolving players and generating pairings."""

from random import shuffle
from typing import List, Tuple

from domain.models.player import Player
from domain.models.round import Round
from domain.models.tournament import Tournament
from domain.ports.player_repository import IPlayerRepository
from infra.utils.round_utils import round_with_loaded_players


def tournament_with_loaded_players(
        tournament: Tournament,
        player_repository: IPlayerRepository
) -> Tournament:
    """
    Return a new Tournament instance with players and rounds fully resolved from their IDs.
    """
    loaded_players: List[Player] = []
    for player_id in tournament.players:
        player = player_repository.get_by_id(player_id)
        if player:
            loaded_players.append(player)
    loaded_rounds: List[Round] = []
    for chess_round in tournament.rounds:
        loaded_rounds. append(round_with_loaded_players(
            chess_round,
            player_repository
        ))
    return Tournament(
        name=tournament.name,
        location=tournament.location,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
        number_of_rounds=tournament.number_of_rounds,
        current_round_number=tournament.current_round_number,
        status=tournament.status,
        rounds=loaded_rounds,
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
    this tournament, based on their national chess id.
    """
    id1 = player1.national_chess_id
    id2 = player2.national_chess_id

    for round_instance in tournament.rounds:
        for match in round_instance.matches:
            p1_id, p2_id = match.get_players()
            if {p1_id, p2_id} == {id1, id2}:
                return True
    return False


def create_pairs_for_next_round(
        tournament: Tournament,
        player_repository: IPlayerRepository
) -> List[Tuple[Player, Player]]:
    """
    Creates pairs for the next round of the tournament.
    Returns a list of (Player, Player) tuples.
    """

    # Ensure all players are full Player objects
    players: List[Player] = [
        p if isinstance(p, Player) else player_repository.get_by_id(p)
        for p in tournament.players
    ]

    # Sort players by descending score
    if tournament.current_round_number == 1:
        # First round: pair players randomly
        shuffle(players)
    else:
        # Other rounds: sort players by descending score
        players.sort(key=lambda p: tournament.scores[p.national_chess_id], reverse=True)

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
                    paired.update(
                        {player.national_chess_id,
                         opponent.national_chess_id}
                    )
                    break

    return pairs
