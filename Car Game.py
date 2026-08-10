import pygame
import sys 
import random

#player class
class Players(pygame.sprite.Sprite):
    def __init__(self,image_name,x,y,speed,width,height):
        super().__init__()
        self.image = pygame.image.load(f"car files/{image_name}")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.width = width
        self.height = height
#player movement
    def inputs(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.y > 0:    
                self.rect.y -= self.speed           
       if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
       if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.y < screen_Height - self.height:
                self.rect.y += self.speed
       if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            if self.rect.x < screen_Width - self.height:
                self.rect.x += self.speed

    def update(self):
        self.inputs()

#Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self,image_name,x,y,speed,width,height):
        super().__init__()
        self.image = pygame.image.load(f"Opponent files/{image_name}")
        self.rect = self.image.get_rect(topleft = (x,y))
        self.speed = speed
        self.width = width
        self.height = height


    def update(self):
        global score
        self.rect.y += self.speed
        if self.rect.y > screen_Height:
            self.rect.x = random.randint(0, screen_Width - self.width)
            self.rect.y = -self.height
            score += 1
            self.speed += 0.5

#Collision physics 
def Collisions(player_group,enemy_group):
    return pygame.sprite.spritecollide(player_group,enemy_group, False)

#screen loading + game background loading
pygame.init()
screen_Width = 1920
screen_Height = 1200
screen_img = pygame.image.load("game_title.png")
screen = pygame.display.set_mode((screen_Width,screen_Height))
road = pygame.image.load("Road.png")
choose_image = pygame.image.load("choose_screen .png")
calm_musik = pygame.mixer.Sound("Dreamspeedrun.mp3")
pygame.display.set_caption("Ryan's Car Game")
calm_musik.play(-1)
clock = pygame.time.Clock()

#color + font
RED = (255,44,44)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 30, bold=True)

#rect for each button 
Startbutton_rect = pygame.Rect(765,540,416,85)
Choosecarbutton_rect = pygame.Rect(765,640,416,85)
Exitbutton_rect = pygame.Rect(765,740,416,85)

Mclaren_Button = pygame.Rect(440,370,269,97)
Buggati_Button = pygame.Rect(690,440,282,93)
Lambo_Button = pygame.Rect(980,430,254,142)
Porsche_Button = pygame.Rect(1270,440,254,85)

#player attributes 
Players_group = pygame.sprite.Group()
Mclaren = Players("mclaren.png",400,440,45,269,97)
Buggati = Players("Buggati.png",690,440,50,282,93)
Lambo = Players("Lamborghini.png",980,430,20,254,142)
Porsche = Players("Porsche.png",1270,440,35,254,85)
Players_group.add(Mclaren,Buggati,Lambo,Porsche)

#enemy attributes
Enemy_group = pygame.sprite.Group()
Stop = Enemy("Stop.png",random.randint(0, screen_Width - 133),random.randint(0, screen_Height - 370),200,133,379)
Enemy_group.add(Stop)

#game state
state = "menu"
score = 0
choose = 0
running = True

def reset():
    global score
    global Enemy_group
    score = 0 
    Enemy_group = pygame.sprite.Group()
    stop_sign =Enemy("Stop.png", random.randint(0, screen_Width - 133), random.randint(0, screen_Height - 379), 4, 133, 379)
    Enemy_group.add(stop_sign)
    if choose != 0:
        choose.rect.topleft = (screen_Width // 2, screen_Height - 200)

while running:
    mouse_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

    keys = pygame.key.get_pressed()

    #character choice trigger
    if state == "menu":
        screen.blit(screen_img, (0,0))
        if mouse_pos:
            if Startbutton_rect.collidepoint(mouse_pos):
                if choose != 0:
                    reset()
                    state = "play"
            elif Choosecarbutton_rect.collidepoint(mouse_pos):
                state = "choose"
            elif Exitbutton_rect.collidepoint(mouse_pos):
                running = False


    elif state == "choose":
        screen.fill(BLACK)
        screen.blit(choose_image, (330,200))
        Players_group.draw(screen)

        if mouse_pos:
            if Mclaren_Button.collidepoint(mouse_pos):
                choose = Mclaren
            elif Buggati_Button.collidepoint(mouse_pos):
                choose = Buggati
            elif Lambo_Button.collidepoint(mouse_pos):
                choose = Lambo
            elif Porsche_Button.collidepoint(mouse_pos):
                choose = Porsche
        if keys[pygame.K_b]:
            state = "menu"
            
            #game trigger
    elif state == "play":
        screen.blit(road,(0,0))
            
        choose.update()
        screen.blit(choose.image, choose.rect)

        Enemy_group.update()
        Enemy_group.draw(screen)

        if Collisions(choose, Enemy_group):
            state = "game over"


    #score display system                
        score_surf = font.render(f"Score: {score}", True, BLACK)
        message_x = 325
        message_y = 200
        screen.blit(score_surf, (message_x,message_y))
    #game restart display    

    
    elif state == "game over":
        screen.blit(road, (0,0))
        over_surf = font.render(f"Final Score: {score}", True, BLACK)
        under_surf = font.render(f"Press 'R' to restart again.", True, BLACK)
        Extra_surf = font.render(f"OR", True, BLACK)
        Back_surf = font.render(f"Press ESC to go back to menu.", True, BLACK)
        
        text_x = (screen_Width // 2) - (over_surf.get_width() // 2)
        text_y = (screen_Height // 2) - (over_surf.get_height() // 2)
        screen.blit(over_surf, (text_x, text_y))
        screen.blit(under_surf, (860,650))
        screen.blit(Extra_surf, (950,695))
        screen.blit(Back_surf, (840,750))

        if keys[pygame.K_r]:
            reset()
            state = "play"
        elif keys[pygame.K_ESCAPE]:
            state = "menu"


#end
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
    
