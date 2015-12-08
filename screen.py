import random
from ship import *
from sdl2 import *


class Screen:
    def __init__(self):
        self.r_target = None
        self.time_elapsed = 0
        self.sndExp = 1
        self.sndMissileLaunch = 2
        self.sndCrash = 3
        self.sndLaser = 4

        r = SDL_Rect()
        r.x = 0
        r.y = 0
        r.w = 640
        r.h = 480
        self.screen_rect = r

        self.window = SDL_CreateWindow(b"Test 5",
                                       SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                       r.w, r.h, SDL_WINDOW_SHOWN)

        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)

        r = self.imageRect = SDL_Rect()
        r.x = 0
        r.y = 0
        r.w = 32
        r.h = 32
        self.textures = []
        for i in range(10):
            sdl_surface = SDL_LoadBMP(((str(i) + ".bmp").encode("utf-8")))
            SDL_SetColorKey(sdl_surface, 1, 0)
            self.textures.append(SDL_CreateTextureFromSurface(self.renderer, sdl_surface))
            SDL_FreeSurface(sdl_surface)

        self.objects = []
        self.ships = []

        self.max_x = self.screen_rect.w
        self.max_y = self.screen_rect.h

        self.player = Ship(self)
        self.player.ai = -1
        self.player.x = self.max_x / 2
        self.player.y = self.max_y

        self.create_group()

        self.stars = []

        self.init_stars()

        self.firing = False
        self.fire_rate = 0
        self.shotgun = False
        self.asrc = True
        self.c_x = 0
        self.c_y = 0
        self.display_cursor = False
        self.fire_side = 1

        self.visible_laser = False
        self.laser_y = 0

    def init_stars(self):
        class Star:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        for i in range(10):
            self.stars.append(Star(random.uniform(0, self.max_x), random.uniform(0, self.max_y)));

    def add(self, o):
        self.objects.append(o)

    def remove(self, o):
        while o in self.objects: self.objects.remove(o)

    def add_ship(self, s):
        self.ships.append(s)

    def remove_ship(self, s):
        self.ships.remove(s)
        while s in self.ships: self.ships.remove(s)

    def create_shot(self, x, y, vx, vy, range, from_explosion):
        shot = Shot(self, x, y, from_explosion)
        shot.xvel = vx
        shot.yvel = vy
        shot.range = range

    def is_hit(self, x, y, exclude):
        ship_size2 = 16 * 16
        for s in self.ships:
            dx = s.x - x
            dy = s.y - y
            if dx ** 2 + dy ** 2 < ship_size2:
                return s
        return None

    def run(self):
        running = True

        while running:
            event = SDL_Event()
            while SDL_PollEvent(event) != 0:
                if event.type == SDL_QUIT:
                    running = False
                    break
                elif event.type == SDL_MOUSEMOTION:
                    self.player.x = event.motion.x
                    self.player.y = event.motion.y
                if event.type == SDL_MOUSEBUTTONDOWN:
                    self.firing = True
                elif event.type == SDL_MOUSEBUTTONUP:
                    self.firing = False
                elif event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == SDLK_RETURN:
                        self.shotgun = not self.shotgun
                    elif event.key.keysym.sym == SDLK_SPACE:
                        self.asrc = not self.asrc

            self.update()
            self.render_scene()

    def game_logic(self):
        player = self.player
        if self.firing and self.fire_rate < 0:
            self.fire_rate = 1
            if self.shotgun:
                from_x = player.x + 16 * self.fire_side
                from_y = player.y - 18
                self.small_explosion(from_x, from_y, 0, -16)
                self.fast_display(from_x, from_y, 5)
                self.fire_side *= -1
                self.play_sound(self.sndMissileLaunch)
            elif self.asrc:
                self.fire_asrc()
            else:
                self.fire_laser()
        else:
            self.fire_rate -= 1

        if self.r_target:
            if self.r_target.hp < 0:
                self.r_target = None

        if self.asrc:
            if self.r_target:
                self.c_x += (self.r_target.x - self.c_x) / 3
                self.c_y += (self.r_target.y - self.c_y) / 3

        if len(self.ships) == 1:
            self.create_group()

    def fire_asrc(self):
        player = self.player
        x = player.x

        for s in self.ships:
            if s != player and s.x - 40 < x < s.x + 46:
                self.r_target = s
                self.small_explosion(self.c_x + random.uniform(-30, 30), self.c_y + random.uniform(-30, 30), 0, 0)
        self.play_sound(self.sndLaser)

    def fire_laser(self):
        self.visible_laser = True
        x = self.player.x
        for s in self.ships:
            if s != self.player and s.x - 15 < x < s.x + 15:
                self.laser_y = s.y
                s.damage(3)
                return
        self.laser_y = 0

    def update(self):

        for s in self.ships:
            s.update()
        for o in self.objects:
            o.update()

        self.game_logic()

    def render_scene(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)

        SDL_RenderClear(self.renderer);
        self.fast_display(100, 40, 2)

        if self.visible_laser:
            self.draw_laser(self.laser_y)
            self.visible_laser = False

        self.draw_stars()

        for s in self.ships:
            s.render()
        for o in self.objects:
            o.render()

        if self.asrc:
            self.fast_display(self.c_x, self.c_y, 6)

        SDL_RenderPresent(self.renderer)
        # SDL_UpdateWindowSurface(self.window)
        SDL_Delay(50)

    def draw_stars(self):
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255)
        for s in self.stars:
            SDL_RenderDrawPoint(self.renderer, int(s.x), int(s.y))
            s.y += 1
            if s.y > self.max_y:
                s.y = 0

    def fast_display(self, x, y, num, center=True):
        dst_rect = self.imageRect.__copy__()
        dst_rect.x = int(x)
        dst_rect.y = int(y)
        if center:
            dst_rect.x -= int(dst_rect.w / 2)
            dst_rect.y -= int(dst_rect.h / 2)

        SDL_RenderCopy(self.renderer, self.textures[num + 1], self.imageRect, dst_rect);

    def draw_laser(self, y):
        SDL_SetRenderDrawColor(self.renderer, 255, 100, 100, 255)
        SDL_RenderDrawLine(self.renderer, int(self.player.x), int(self.player.y), int(self.player.x), int(y))

    def explosion(self, x, y):
        for i in range(20):
            self.create_shot(x, y, random.uniform(-10, 10), random.uniform(-10, 10),
                             random.uniform(10, 20), True)

        self.play_sound(self.sndExp)

    def small_explosion(self, x, y, vx, vy):
        for i in range(5):
            self.create_shot(x, y, random.uniform(-2, 2) + vx, random.uniform(-2, 2) + vy,
                             random.uniform(10, 20), True)
        self.play_sound(self.sndCrash)

    def create_group(self):
        group = {}
        for i in range(5 + int(self.time_elapsed / 3)):
            s = Ship(self)
            s.hp = 10
            s.x = random.uniform(50, self.max_x - 50)
            s.y = random.uniform(-20, 80)
            s.set_pic(1)
            group[i] = s

        s = Ship(self)
        s.hp = 10
        s.ai = 2
        s.ai_data = 0
        s.x = 380
        s.y = -20
        s.set_pic(7)
        group[6] = s

        self.time_elapsed += 1

        if self.time_elapsed < 10:
            return

        if random.random() > .8:
            s = Ship(self)
            s.hp = 50
            s.ai = 3
            s.ai_data = 0
            s.x = random.uniform(0, self.max_x)
            s.set_pic(8)

    def play_sound(self, sound):
        pass


screen = Screen();

screen.run()
