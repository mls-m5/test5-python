from math import sqrt


class Shot:
    def __init__(self, screen, x, y, from_explosion=0, target=None, exclusion=None):
        self.x = x
        self.y = y
        self.xvel = 0
        self.yvel = 0
        self.exclusion = exclusion
        self.from_explosion = from_explosion
        self.target = target
        self.screen = screen
        self.range = 10
        screen.add(self)

    def render(self):
        s = self.screen
        s.fast_display(self.x - self.xvel * 4, self.y - self.yvel * 4, 4)
        s.fast_display(self.x - self.xvel * 2, self.y - self.yvel * 2, 3)
        s.fast_display(self.x, self.y, 2)
        s.fast_display(self.x - self.xvel, self.y - self.yvel, 2)
        s.fast_display(self.x - self.xvel * 3, self.y - self.yvel * 3, 3)

    def update(self):
        hit = self.screen.is_hit(self.x, self.y, self.exclusion)
        if hit:
            hit.damage(3)
            self.screen.remove(self)
            if not self.from_explosion:
                screen.small_explosion(self.x - self.xvel, self.y - self.yvel, -self.xvel / 3, -self.yvel / 3)
        if self.target:
            t = self.target

            x = self.x
            y = self.y
            if t.x + 16 != x and y + 16 != t.y:
                dx = t.x - self.x
                dy = t.y - self.y
                if dx * self.xvel + dy * self.yvel > 0:  # if the target is in front of the shot
                    dist = sqrt(dx ** 2 + dy ** 2)

                    self.xvel = dx / dist * 20 + t.xvel
                    self.yvel = dy / dist * 20 + t.yvel
        self.x += self.xvel
        self.y += self.yvel

        self.range -= 1
        if self.range < 0:
            self.screen.remove(self)
            self.screen.fast_display(self.x, self.y, 5)

        if self.from_explosion == 2:
            self.screen.explosion(self.x, self.y)
