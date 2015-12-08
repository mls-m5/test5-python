from shot import Shot
from math import sqrt
from ai import AI


class Ship:
    def __init__(self, screen):
        self.hp = 100
        self.ai = 1
        self.ai_object = AI(screen, self)
        self.x = 0
        self.y = 0
        self.xvel = 0
        self.yvel = 0
        self.pic = 0
        self.screen = screen

        self.fire_rate = 0

        screen.add_ship(self)

    def set_pic(self, number):
        self.pic = number

    def set_player(self):
        self.ai = 0

    def render(self):
        self.screen.fast_display(self.x, self.y, self.pic)

    def update(self):
        self.x += self.xvel
        self.y += self.yvel

        if self.ai >= 0:
            self.ai_object.move(self.ai)

        if self.y > self.screen.max_y:
            self.screen.explosion(self.x, self.y)

    def damage(self, value):
        self.hp -= value
        if self.hp < 0:
            self.screen.remove_ship(self)
            self.screen.explosion(self.x, self.y)

    def fire(self, rate, target=None):
        if self.fire_rate > 0:
            self.fire_rate -= 1
            return
        self.fire_rate = rate

        shot = Shot(self.screen, self.x, self.y + 40, self, target)

        player = self.screen.player

        dx = player.x - self.x
        dy = player.y - self.y - 15

        total = sqrt(dx ** 2 + dy ** 2)
        shot.xvel = dx / total * 15
        shot.yvel = dy / total * 15

        shot.range = 100

        # screen.play_sound()
        # frmScreen.PlaySound frmScreen.sndEnemyshot
