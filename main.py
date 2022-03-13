import random

import pygame

WINDOW_TITLE = 'BUSMatchThree'
FPS = 60
SCREEN_WEIGHT, SCREEN_HEIGHT = 600, 600


class Element(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = x, y


class Field(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)


class Game:

    def __init__(self, size):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('audio/music.mp3')
        self.window = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.elements_images = [
            pygame.transform.scale(pygame.image.load(x), (SCREEN_HEIGHT // size, SCREEN_HEIGHT // size)) for x in (
                'images/asm.png',
                'images/js.png',
                'images/python.png',
                'images/cs.png',
                'images/cpp.png',
                'images/php.png',
                'images/java.png',
            )
        ]
        self.elements = Field()
        self.size = size
        self.selected_elements = []
        self.line_points = []
        self.is_line_input = False

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
                            self.elements.remove(el)
                self.line_points = []
                self.selected_elements = []
                self.is_line_input = False

        if self.is_line_input:
            pos = pygame.mouse.get_pos()
            for el in self.elements:
                if el.rect.collidepoint(*pos):
                    center = el.rect.center
                    if center not in self.line_points:
                        self.line_points.append(center)
                    if el not in self.selected_elements:
                        self.selected_elements.append(el)

        self.window.fill((0, 0, 0))
        self.elements.draw(self.window)
        if len(self.line_points) > 1:
            pygame.draw.lines(self.window, (255, 255, 255), False, self.line_points, 10)
        pygame.display.flip()

    def run(self):
        element_size = SCREEN_HEIGHT // self.size
        for y in range(0, SCREEN_HEIGHT, element_size):
            for x in range(0, SCREEN_HEIGHT, element_size):
                self.elements.add(Element(x, y, random.choice(self.elements_images)))

        pygame.mixer.music.play(-1)
        while self.running:
            self.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game(10).run()
