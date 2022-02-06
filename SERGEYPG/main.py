import os
import sys
import pygame
import random

score = 0
with open('best_score', 'r', encoding='utf-8') as file:
    bscore = int(file.readline())


class Stone(pygame.sprite.Sprite):
    def __init__(self, app):
        pygame.sprite.Sprite.__init__(self)
        self.image = app.load_image("stone.png")
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .45 / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(app.width - self.rect.width)

    def update(self, app, z):
        self.rect.y += app.speed
        if z == 0:
            self.kill()


class Exlife(pygame.sprite.Sprite):
    def __init__(self, app):
        pygame.sprite.Sprite.__init__(self)
        self.image = app.load_image("exlife.png")
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .45 / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(app.width - self.rect.width)

    def update(self, app, z):
        self.rect.y += app.speed
        if z == 0:
            self.kill()


class Tile(pygame.sprite.Sprite):
    def __init__(self, app, tile_type, pos_x, pos_y):
        super().__init__(app.tiles_group, app.all_sprites)
        if tile_type == 'empty':
            self.image = app.load_image('fon_v_igre.jpg')
        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x, app.tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, app, pos_x, pos_y):
        super().__init__(app.player_group, app.all_sprites)
        self.image = app.load_image("pers1.png")
        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x + 15, app.tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if x == 0 and y == 0:
            self.kill()
        if self.rect.right > app.width - 17:
            self.rect.right = app.width - 17
        if self.rect.left < -17:
            self.rect.left = -17
        if self.rect.top < 3:
            self.rect.top = 3
        if self.rect.bottom > app.height + 3:
            self.rect.bottom = app.height + 3


class Hearts(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = app.load_image("heart.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 550, 550
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Treasure Hunter')
        self.fps = 0
        pygame.key.set_repeat(200, 70)
        self.colide = pygame.mixer.Sound('data/colide.mp3')
        self.fon_m =  pygame.mixer.Sound('data/fon_m.mp3')
        self.exlife_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()
        self.speed = 3
        self.hp = 3
        self.score = 0
        self.bscore = bscore
        self.OWNEVENT = 30
        self.EXLEVENT = 3
        self.SCEVENT = 5
        self.hero = None
        self.tile_width = self.tile_height = 50
        self.player, self.level_x, self.level_y = self.generate_level(self.load_level('level_1.txt'))

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def music_play(self, name):
        pygame.mixer.init()
        pygame.mixer.init()
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Звуковой файл '{fullname}' не найден")
            sys.exit()
        pygame.mixer.music.load(fullname)

    def run_game(self):
        pygame.time.set_timer(self.OWNEVENT, 300)
        pygame.time.set_timer(self.EXLEVENT, 20000)
        pygame.time.set_timer(self.SCEVENT, 200)
        self.music_play('fon_m.mp3')
        pygame.mixer.music.play(-1)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause_screen()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_DOWN] or key[pygame.K_s]:
                        self.player.update(0, 7)
                    if key[pygame.K_LEFT] or key[pygame.K_a]:
                        self.player.update(-7, 0)
                    if key[pygame.K_RIGHT] or key[pygame.K_d]:
                        self.player.update(7, 0)
                    if key[pygame.K_UP] or key[pygame.K_w]:
                        self.player.update(0, -7)
                if event.type == self.OWNEVENT:
                    self.stone_group.add(Stone(self))
                if event.type == self.EXLEVENT:
                    self.exlife_group.add(Exlife(self))
                if event.type == self.SCEVENT:
                    self.score += 1
            clash = pygame.sprite.spritecollide(self.player, self.stone_group, True, pygame.sprite.collide_mask)
            if clash:
                self.colide.play()
                self.hp -= 1
                if self.hp == 0:
                    self.end_screen()

            exstrlife = pygame.sprite.spritecollide(self.player, self.exlife_group, True, pygame.sprite.collide_mask)
            if exstrlife:
                if self.hp < 3:
                    self.hp += 1
                    b = 1

            # render
            self.screen.fill(pygame.Color('blue'))
            self.tiles_group.draw(self.screen)
            self.player_group.draw(self.screen)
            self.stone_group.draw(self.screen)
            self.stone_group.update(self, 1)
            self.exlife_group.draw(self.screen)
            self.exlife_group.update(self, 1)
            self.score_in_game(30, self.width / 2, 10)
            self.hearts(30, self.width - 50, 10)
            self.clock.tick(self.fps)
            pygame.display.flip()

    def hearts(self, size, a, b):
        font_name = pygame.font.match_font('None')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(f'{self.hp}', True, 'red')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (a, b)
        self.screen.blit(text_surface, text_rect)

    def score_in_game(self, size, a, b):
        font_name = pygame.font.match_font('None')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(f'{self.score}', True, 'black')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (a, b)
        self.screen.blit(text_surface, text_rect)

    def best_score(self):
        if self.bscore < self.score:
            self.bscore = self.score
        with open('best_score', 'w', encoding='utf-8') as file:
            file.write(str(self.bscore))
        file.close()

    def start_screen(self):
        intro_text = ["Treasure Hunter", "", "", "",
                      "ИСПОЛЬЗУЙТЕ СТРЕЛОЧКИ ДЛЯ ДВИЖЕНИЯ", "",
                      f"ЛУЧШИЙ СЧЁТ    {self.bscore}", "", "", "", "", "", "",
                      "НАЖМИТЕ ЧТОБЫ ИГРАТЬ"]

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.run_game()  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)

    def pause_screen(self):
        intro_text = ["ПАУЗА", "", "", "",
                      "", "",
                      "", "", "", "", "", "", "",
                      "НАЖМИТЕ Esc ЧТОБЫ ПРОДОЛЖИТЬ",
                      "НАЖМИТЕ Backspace ЧТОБЫ ВЫЙТИ"]

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.run_game()  # начинаем игру
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.start_screen()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def end_screen(self):
        self.best_score()
        self.player.kill()
        self.stone_group.update(self, 0)
        self.hp = 3
        intro_text = [f"ВАШ СЧЁТ   {self.score}", "",
                      f"ЛУЧШИЙ СЧЁТ  {self.bscore}",
                      "", "", "", "", "", "",
                      "", "", "",
                      "НАЖМИТЕ Esc, ЧТОБЫ ВЫЙТИ",
                      "НАЖМИТЕ R, ЧТОБЫ НАЧАТЬ СНАЧАЛА"]

        fon = pygame.transform.scale(self.load_image('gmov.png'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        self.score = 0
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        self.player, self.level_x, self.level_y = self.generate_level(self.load_level('level_1.txt'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.run_game()  # начинаем заново игру
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.start_screen()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def load_level(self, filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '#':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '@':
                    Tile(self, 'empty', x, y)
                    new_player = Player(self, x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y


if __name__ == '__main__':
    app = App()
    app.start_screen()
    app.run_game()