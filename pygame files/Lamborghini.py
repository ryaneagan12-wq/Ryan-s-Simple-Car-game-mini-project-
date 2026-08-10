import pygame
import sys
import random


pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
screen_img = pygame.image.load("Road.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(screen_img, (0,0))
pygame.display.set_caption("Speedy Mclaren")
clock = pygame.time.Clock()

SKY_BLUE = (224,247,250)
TEXT_BLACK = (0, 0, 0)

player_width = 324  
player_height = 180
player_x = 800
player_y = 800
player_speed = 70

enemy_width = 133
enemy_height = 379
enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 100

Lamborghini_img = pygame.image.load("Lamborghini.png")
Lamborghini = pygame.transform.scale(Lamborghini_img, (player_width, player_height))

stop_img = pygame.image.load("Stop.png")
stop = pygame.transform.scale(stop_img, (enemy_width, enemy_height))


score = 0
font = pygame.font.SysFont("Arial", 24, bold=False)

game_over = False
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if player_y > 0:    
                    player_y -= player_speed           
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if player_x > 0:
                    player_x -= player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if player_y < SCREEN_HEIGHT - player_height:
                    player_y += player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
                if player_x < SCREEN_WIDTH - player_height:
                    player_x += player_speed
        
        if not game_over:
            enemy_y += enemy_speed
            if enemy_y > SCREEN_HEIGHT:
                enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
                enemy_y = -enemy_height
                score += 1
                enemy_speed += 0.5
                
            position_x = player_x + (player_width // 2)
            position_y = player_y - player_height
            if (position_x < enemy_x + enemy_width and position_x + enemy_width> enemy_x and position_y < enemy_y + enemy_height and position_y + enemy_height > enemy_y):
                game_over = True

        screen.blit(screen_img, (0,0))
        screen.blit(Lamborghini, (player_x, player_y))
        screen.blit(stop, (enemy_x, enemy_y ))
       
        if not game_over:
            score_surf = font.render(f"Score: {score}", True, TEXT_BLACK)
            message_x = 325
            message_y = 200
            screen.blit(score_surf, (message_x,message_y))
        else:
            over_surf = font.render(f"Final Score: {score}", True, TEXT_BLACK)
            under_surf = font.render(f"Press 'R' to restart again.", True, TEXT_BLACK)
            Extra_surf = font.render(f"OR", True, TEXT_BLACK)
            Back_surf = font.render(f"Press Alt + F4 to Quit Game.", True, TEXT_BLACK)
            text_x = (SCREEN_WIDTH // 2) - (over_surf.get_width() // 2)
            text_y = (SCREEN_HEIGHT // 2) - (over_surf.get_height() // 2)
            screen.blit(over_surf, (text_x, text_y))
            screen.blit(under_surf, (860,650))
            screen.blit(Extra_surf, (950,695))
            screen.blit(Back_surf, (840,750))
            
            if keys[pygame.K_r] == 1:
                player_x = 800
                player_y = 800
                score = 0
                running = True
                game_over = False

        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
