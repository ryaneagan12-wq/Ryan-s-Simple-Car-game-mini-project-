import pygame
import random
import sys

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
screen_img = pygame.image.load("Road.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(screen_img, (0,0))
pygame.display.set_caption("Ryan's Car Game")
clock = pygame.time.Clock()

TEXT_BLACK = (0, 0, 0)

player_size = 300  
player_x = 800
player_y = 800
player_speed = 10
mclaren_img = pygame.image.load("Lamborghini.png").convert_alpha()
mclaren = pygame.transform.scale(mclaren_img, (player_size, player_size))

StopSign_img = pygame.image.load("Stop.png").convert_alpha()
enemy_size = 300
enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)
enemy_y = -enemy_size
enemy_speed = 8
StopSign = pygame.transform.scale(StopSign_img, (enemy_size, enemy_size))


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
            if player_y < SCREEN_HEIGHT - player_size:
                player_y += player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            if player_x < SCREEN_WIDTH - player_size:
                player_x += player_speed
        
        if not game_over:
            enemy_y += enemy_speed
            if enemy_y > SCREEN_HEIGHT:
                enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)
                enemy_y = -enemy_size
                score += 1
                enemy_speed += 0.5

            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
            if player_rect.colliderect(enemy_rect):
                game_over = True

        screen.blit(screen_img, (0,0))
        screen.blit(mclaren, (player_x, player_y))
        screen.blit(StopSign, (enemy_x, enemy_y ))
       
        if not game_over:
            score_surf = font.render(f"Score: {score}", True, TEXT_BLACK)
            message_x = 325
            message_y = 200
            screen.blit(score_surf, (message_x,message_y))
        else:
            over_surf = font.render(f"Final Score: {score}", True, TEXT_BLACK)
            text_x = (SCREEN_WIDTH // 2) - (over_surf.get_width() // 2)
            text_y = (SCREEN_HEIGHT // 2) - (over_surf.get_height() // 2)
            screen.blit(over_surf, (text_x, text_y))
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
