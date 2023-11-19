from chicken_game.player import player

class game():
    def __init__(self,player_count=2):
        self.players = [player() for i in range(2)]
    def run(self,display=None):
        for i in range(10):
            self.players[0].position[1][0]-=5
            print(self.players[0].position,len(self.players))
        print("Game ended.")
