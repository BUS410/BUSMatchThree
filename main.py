import os
import random

import pygame

WINDOW_TITLE = 'BUSMatchThree'
FPS = 60
SCREEN_WEIGHT, SCREEN_HEIGHT = 600, 600


class Element(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def sub_rect(self):
        border_size = self.rect.width // 10
        return pygame.rect.Rect(self.rect.x + border_size, self.rect.y + border_size,
                                self.rect.width - border_size * 2, self.rect.height - border_size * 2)


class Field(pygame.sprite.Group):

    def __init__(self, size: int):
        pygame.sprite.Group.__init__(self)
        self._table: list[list[Element | None]] = [[None for _ in range(size)] for _ in range(size)]
        self.element_size = SCREEN_HEIGHT // size
        self.elements_images = [
            pygame.transform.scale(pygame.image.load(f'images/{x}'),
                                   (SCREEN_HEIGHT // size, SCREEN_HEIGHT // size)) for x in os.listdir('images')
        ]

    def create(self):
        self.empty()
        for y in range(0, SCREEN_HEIGHT, self.element_size):
            for x in range(0, SCREEN_HEIGHT, self.element_size):
                self.add(Element(x, y, random.choice(self.elements_images)))

    def add(self, *sprites):
        pygame.sprite.Group.add(self, *sprites)
        for sprite in sprites:
            self._table[sprite.rect.y // self.element_size][sprite.rect.x // self.element_size] = sprite

    def remove(self, *sprites):
        pygame.sprite.Group.remove(self, *sprites)
        for el in sprites:
            if el in sprites:
                for y, line in enumerate(self._table):
                    for x, obj in enumerate(line):
                        if obj is el:
                            self._table[y][x] = None

    def drop(self):
        while not all(all(line) for line in self._table):
            for y, line in enumerate(self._table):
                for x, el in enumerate(line):
                    if el is None:
                        if y > 0:
                            self._table[y - 1][x].rect.y += self.element_size
                            self._table[y][x] = self._table[y - 1][x]
                            self._table[y - 1][x] = None
                        else:
                            self._table[y][x] = Element(x * self.element_size, y * self.element_size,
                                                        random.choice(self.elements_images))
                            self.add(self._table[y][x])


class Game:

    def __init__(self, size):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('audio/music.mp3')
        self.pop_sound = pygame.mixer.Sound('audio/pop.wav')
        self.window = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.field = Field(size)
        self.size = size
        self.selected_elements = []
        self.line_points = []
        self.is_line_input = False
        self.score = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.is_line_input = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if len(self.selected_elements) >= 3:
                    el_image = self.selected_elements[0].image
                    for el in self.selected_elements[1:]:
                        if el.image is not el_image:
                            break
                    else:
                        for el in self.selected_elements:
                            self.field.remove(el)
                        self.pop_sound.play()
                        self.score += 2 ** len(self.line_points)
                self.line_points = []
                self.selected_elements = []
                self.is_line_input = False
                self.field.drop()

        if self.is_line_input:
            pos = pygame.mouse.get_pos()
            for el in self.field:
                if el.sub_rect().collidepoint(*pos):
                    center = el.rect.center
                    if center not in self.line_points:
                        self.line_points.append(center)
                    if el not in self.selected_elements:
                        self.selected_elements.append(el)

        self.field.update()

        self.window.fill((32, 32, 32))
        self.field.draw(self.window)
        if len(self.line_points) > 1:
            pygame.draw.lines(self.window, (255, 255, 255), False, self.line_points, 10)
        pygame.display.set_caption(f'{WINDOW_TITLE}.    Score: {self.score}')
        pygame.display.flip()

    def run(self):

        pygame.mixer.music.play(-1)
        self.field.create()
        while self.running:
            self.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game(10).run()
