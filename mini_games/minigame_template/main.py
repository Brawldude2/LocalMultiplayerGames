from minigame_template.module import template_function

class game():
    def __init__(self,player_count,*args):
        self.frame = 0
        self.player_count = player_count
        
    def update(self):
        pass
    def render(self,display):
        pass      
    def run_frame(self,display=None,inputs=None):
        self.update()
        self.render(display)
