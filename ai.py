import random


class AI:
    def __init__(self, screen, ship):
        self.ship = ship
        self.screen = screen
        self.data = 0
        self.strategies = [None, self.strategy1, self.strategy2, self.strategy3]

    def move(self, move_variant):
        self.strategies[move_variant]()

    def strategy1(self):
        s = self.ship
        player = self.screen.player

        bottom = self.screen.max_y
        width = self.screen.max_x

        if self.data == 6:
            if s.y > bottom / 3:
                s.yvel -= 1
            else:
                s.yvel += 1
            if s.x > player.x:
                s.xvel -= 1
            else:
                s.xvel += 1
            s.fire(40)
            if s.x < 0:
                s.xvel = 1
            if s.x > width:
                s.xvel = -1
        elif self.data == 5:
            s.yvel = 2
            s.xvel = 0
            if s.y > bottom / 1.5:
                self.data = 4
        elif self.data == 4:
            s.yvel = 0
            self.data = 6
        elif self.data == 3:
            s.xvel = 0
            s.yvel = 2
            s.fire(50)
            if s.y > bottom / 4:
                self.data = 5
        elif self.data == 2:
            s.yvel = 3
            if player.x > s.x:
                s.xvel = 1
            else:
                s.xvel = -1
            s.fire(50)
            if s.y > bottom / 5:
                self.data = 3
        elif self.data == 1:
            s.yvel = 4
            if s.y > 150:
                self.data = 2
        elif self.data == 0:
            s.yvel = 6
            if s.y > bottom / 12:
                self.data = 1

    def strategy2(self):
        s = self.ship
        player = self.screen.player
        bottom = self.screen.max_y
        width = self.screen.max_x

        if self.data == 0:
            s.yvel = 2
            if s.y > bottom / 4:
                self.data = 1
                s.xvel = -3
                s.yvel = 0
        elif self.data == 1:
            if s.x > width - 32:
                s.xvel = -3
            elif s.x < 0:
                s.xvel = 3
            if random.random() > 0.7:
                s.fire(10, player)
            else:
                s.fire(10)
            #if s.y < 180:
            #    self.data = 0

    def strategy3(self):
        s = self.ship
        player = self.screen.player
        if self.data == 0:
            r = random.random()
            s.yvel = 6
            self.screen.create_shot(s.x - 15, s.y + 15, 20 * r - 10, 20, 20, 1)
            self.screen.create_shot(s.x + 15, s.y + 15, 20 * r - 10, 20, 20, 1)
            if s.x > player.x:
                s.xvel = -10
            else:
                s.xvel = 10
            if player.x - 16 < s.x < player.y + 16:
                s.xvel = 0
