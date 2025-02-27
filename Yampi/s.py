import pygame
import math
import random
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * 64
        self.y = y * 64
        self.width = 64
        self.height = 64

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1

        self.image = pygame.image.load('idle1.png')
        Player.image = self.image
        Player.rect = Player.image.get_rect()
        Player.rect.x = self.x 
        Player.rect.y = self.y
    
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += 3
            self.x_change -= 3
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= 3
            self.x_change += 3
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += 3
            self.y_change -= 3
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= 3
            self.y_change += 3
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += 3
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= 3

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += 3
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= 3

    def animate(self): 
        down_animations = [pygame.image.load('walk1.png'),
                           pygame.image.load('walk2.png'),
                           pygame.image.load('walk3.png'),
                           pygame.image.load('walk4.png'),
        ]

        up_animations = [pygame.image.load('walk up1.png'),
                         pygame.image.load('walk up2.png'),
                         pygame.image.load('walk up3.png'),
                         pygame.image.load('walk up4.png'),
        ]

        right_animations = [pygame.image.load('walk right1.png'),
                            pygame.image.load('walk right2.png'),
                            pygame.image.load('walk right3.png'),
                            pygame.image.load('walk right4.png'),
        ]

        left_animations = [pygame.image.load('walk left1.png'),
                           pygame.image.load('walk left2.png'),
                           pygame.image.load('walk left3.png'),
                           pygame.image.load('walk left4.png'),
        ]



        if self.facing == 'down':
            if self.y_change == 0:
                self.image = pygame.image.load('walk1.png')
                self.image = self.image
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = pygame.image.load('walk up1.png')
                self.image = self.image
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = pygame.image.load('walk left1.png')
                self.image = self.image
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = pygame.image.load('walk right1.png')
                self.image = self.image
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * 64
        self.y = y * 64
        self.width = 64
        self.height = 64

        self.image = pygame.image.load('enemyidle.png')
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(32, 40)

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= 1
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += 1
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        left_animations = [
            pygame.image.load('walk left1.png'),
            pygame.image.load('walk left2.png'),
            pygame.image.load('walk left3.png'),
            pygame.image.load('walk left4.png'),
        ]

        right_animations = [
            pygame.image.load('walk right1.png'),
            pygame.image.load('walk right2.png'),
            pygame.image.load('walk right3.png'),
            pygame.image.load('walk right4.png'),
        ]

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = pygame.image.load('idle1.png')
                self.image = self.image
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = pygame.image.load('idle1.png')
                self.image = self.image
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * 64
        self.y = y * 64
        self.width = 64
        self.height = 64
        self.x_change = 0
        self.y_change = 0

        self.image = pygame.image.load('grass.png')
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('AKONY.otf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    

# class Attack(pygame.sprite.Sprite):