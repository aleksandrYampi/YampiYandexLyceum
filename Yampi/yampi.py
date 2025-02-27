import pygame
from s import *
import sys
from config import *


class Yampi:
    def __init__(self):
        pygame.init()
        self.size = width, height = 1280, 768
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('AKONY.otf', 128)
        self.intro_background = pygame.image.load('intro.png')
        self.running = True
        pygame.display.set_icon(pygame.image.load('yampi_logo.png'))
        self.go_background = pygame.image.load('gg.png')
        pygame.display.set_caption('Yampi')
    
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                     Player(self, j, i)


    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((80, 155, 102))
        self.all_sprites.draw(self.screen)
        self.clock.tick(60)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('GG', True, (255, 255, 255))
        text_rect = text.get_rect(center=(640, 390))
        
        restart_button = Button(470, 435, 340, 50, (0, 0, 0),  (255, 255, 255), 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(60)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        title = self.font.render('Yampi', True, (255, 255, 255))
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 121, 785, 50, (0, 0, 0), (255, 255, 255), 'Play', 16)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(60)
            pygame.display.update()

y = Yampi()
y.intro_screen()
y.new()
while y.running:
    y.main()
    y.game_over()

pygame.quit()
sys.exit()
