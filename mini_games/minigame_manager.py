from tank_game.main     import Game as tank_game
from chicken_game.main  import game as chicken_game

def get_minigame(game_number,player_count,*args):
    if game_number == 1:
        return tank_game(player_count,*args)
    elif game_number == 2:
        return chicken_game(player_count,*args)

