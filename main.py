from configuration import *
from weapons import *
from sprites import *
import sys
import pygame
import pygame.mixer


class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()
    
    def get_image(self, x,y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.spritesheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)
        
        return sprite
class Game:
    
    def __init__(self):
        pygame.init()

        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.terrain_spritesheet = Spritesheet('assets/images/terrain.png') #991,541
        self.player_spritesheet = Spritesheet('assets/images/cats.png')
        self.enemy_spritesheet = Spritesheet('assets/images/evil.png')
        self.weapon_spritesheet = Spritesheet('assets/images/sword.png')
        self.bullet_spritesheet = Spritesheet('assets/images/powerBall.png')
        self.running = True
        self.enemy_collided =False
        self.block_collided = False
        self.restart_button = pygame.Rect(WIN_WIDTH // 2 - 50, WIN_HEIGHT // 2 + 50, 100, 50)

        
        pygame.mixer.music.load('assets/sounds/battleThemeA.mp3')
        self.shooting_sound = pygame.mixer.Sound('assets/sounds/laser2.wav')
        
        
    def createTileMap(self):
        for i, row in enumerate(tilemap):
            for j , column in enumerate(row):
                Ground(self,j,i)
                if column=='B':
                    Block(self,j,i)
                if column=='P':
                    self.player=Player(self,j,i)
                if column=="E":
                    Enemy(self,j,i)
                if column =="R":
                    Water(self,j,i)
                if column =="W":
                    Weapon(self,j,i)
    
    
    def create(self):
        self.all_sprites =pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.water =  pygame.sprite.LayeredUpdates()
        self.enemies= pygame.sprite.LayeredUpdates()
        self.mainPlayer = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.healthbar = pygame.sprite.LayeredUpdates()
        self.createTileMap()
        self.all_sprites.add(self.bullets)  
        pygame.mixer.music.play(-1)
    
    def update(self):
        self.all_sprites.update()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                    self.shooting_sound.play()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def shoot(self):
        self.game.shooting_sound.play()
        bullet = Bullet(self.game, self.rect.centerx, self.rect.top)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

    
    def camera(self):
        if self.enemy_collided==False and self.block_collided==False:
            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_LEFT]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.x += PLAYER_STEPS
    
            elif pressed[pygame.K_RIGHT]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.x -= PLAYER_STEPS
                    
            elif pressed[pygame.K_UP]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.y += PLAYER_STEPS     
                    
            elif pressed[pygame.K_DOWN]:
                for i, sprite in enumerate(self.all_sprites):
                    sprite.rect.y -= PLAYER_STEPS   
    
    def game_over_screen(self):
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        restart_text = font.render("Restart", True, (0, 255, 0))
        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        pygame.draw.rect(self.screen, (0, 0, 255), self.restart_button)
        self.screen.blit(restart_text, restart_text_rect)
        
        pygame.display.update()
        


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.restart_button.collidepoint(event.pos):
                    self.__init__()
                    self.create()
                    return  
                    
            pygame.time.Clock().tick(FPS)
        
                
    def main(self):
        while self.running:
            self.events()
            self.camera()
            self.update()
            self.draw()

            if self.player.health <= 0:
                self.game_over_screen()
        
        pygame.mixer.music.stop()
    
    


game = Game()
game.create()

while game.running:
    game.main()
    
pygame.quit()
sys.exit()
