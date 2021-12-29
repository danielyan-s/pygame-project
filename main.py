import os
import sys
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, app, tile_type, pos_x, pos_y):
        super().__init__(app.tiles_group, app.all_sprites)
        if tile_type == 'wall':
            self.image = app.load_image('box.png')
        elif tile_type == 'empty':
            self.image = app.load_image('grass.png')
            app.load_image('box.png')

        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x, app.tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, app, pos_x, pos_y):
        super().__init__(app.player_group, app.all_sprites)
        self.image = app.load_image("mar.png")
        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x + 15, app.tile_height * pos_y + 5)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Hero(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        super().__init__(app.all_sprites)
        self.image = app.load_image("mar.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
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
        pygame.display.set_caption('Mario')
        self.fps = 50
        pygame.key.set_repeat(200, 70)
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.hero = None
        self.tile_width = self.tile_height = 50


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

    def run_game(self):
        run = True
        self.game_over = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_DOWN]:
                        self.player.update(0, 50)
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_LEFT]:
                        self.player.update(-50, 0)
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_RIGHT]:
                        self.player.update(50, 0)
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_UP]:
                        self.player.update(0, -50)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.game_over += 1
                if self.game_over == 5:
                    self.start_screen()
                    run = False
            # update

            # render
            self.screen.fill(pygame.Color('blue'))
            self.tiles_group.draw(self.screen)
            self.player_group.draw(self.screen)
            # изменяем ракурс камеры
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_screen(self):
            intro_text = ["ЗАСТАВКА", "",
                          "Правила игры",
                          "Если в правилах несколько строк,",
                          "приходится выводить их построчно"]

            fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
            self.screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
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
                        return  # начинаем игру
                pygame.display.flip()
                self.clock.tick(self.fps)




if __name__ == '__main__':
    app = App()
    app.start_screen()
    app.run_game()