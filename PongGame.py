import pygame, sys, random

def reset_ball():
    global ball_speed_x, ball_speed_y, player_hit_ball, cpu_hit_ball
    ball.x = SCREEN_WIDTH / 2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])
    
    player_hit_ball = False
    cpu_hit_ball = False

def point_won(winner):
    global player_points, cpu_points
    if winner == 'cpu':
        cpu_points += 1
    if winner == 'player':
        player_points += 1
    score_sound.play()
    reset_ball()

def animate_ball():
    global ball_speed_x, ball_speed_y, player_hit_ball, cpu_hit_ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.bottom >= SCREEN_HEIGHT or ball.top <= 0:
        ball_speed_y *= -1
        hit_sound.play()
    if ball.right >= SCREEN_WIDTH:
        point_won('cpu')
    if ball.left <= 0:
        point_won('player')
        
    if ball.colliderect(player):
        player_hit_ball = True
        cpu_hit_ball = False
        ball_speed_x *= -1
        hit_sound.play() 
    if ball.colliderect(cpu):
        player_hit_ball = False
        cpu_hit_ball = True
        ball_speed_x *= -1
        hit_sound.play()

def animate_player():
    global player_speed, player_hit_ball
    
    if ball.centerx > SCREEN_WIDTH / 2 and player_hit_ball == False:
        if player.centery > ball.centery:
            player_speed = -6
        elif player.centery < ball.centery:
            player_speed = 6
        else:
            player_speed = 0
    else:
        player_speed = 0

    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def animate_cpu():
    global cpu_speed, cpu_hit_ball
    
    if ball.centerx < SCREEN_WIDTH / 2 and cpu_hit_ball == False:
        if cpu.centery > ball.centery:
            cpu_speed = -6
        elif cpu.centery < ball.centery:
            cpu_speed = 6
        else:
            cpu_speed = 0
    else:
        cpu_speed = 0

    cpu.y += cpu_speed

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= SCREEN_HEIGHT:
        cpu.bottom = SCREEN_HEIGHT

pygame.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600
FPS = 144

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

clock = pygame.time.Clock()

ball = pygame.Rect(0, 0, 30, 30)
ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

cpu = pygame.Rect(10, 0, 20, 100)
cpu.centery = SCREEN_HEIGHT / 2

player = pygame.Rect(0, 0, 20, 100)
player.midright = (SCREEN_WIDTH - 10, SCREEN_HEIGHT / 2) 

ball_speed_x = 7
ball_speed_y = 7
player_speed = 0 
cpu_speed = 0    

player_points, cpu_points = 0, 0
score_font = pygame.font.Font(None, 100)

player_hit_ball, cpu_hit_ball = False, False

hit_sound_filepath = "src/sound/hit_sound.mp3"
score_sound_filepath = "src/sound/score_sound.mp3"
hit_sound = pygame.mixer.Sound(hit_sound_filepath)
score_sound = pygame.mixer.Sound(score_sound_filepath)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    animate_ball()
    animate_player()
    animate_cpu()

    screen.fill('black')
    pygame.draw.aaline(screen, 'white', (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    pygame.draw.ellipse(screen, 'white', ball)
    pygame.draw.rect(screen, 'red', cpu)
    pygame.draw.rect(screen, 'blue', player)
    
    cpu_score_surface = score_font.render(str(cpu_points), True, 'white')
    player_score_surface = score_font.render(str(player_points), True, 'white')
    screen.blit(cpu_score_surface, (SCREEN_WIDTH / 4, 20))
    screen.blit(player_score_surface, (3 * SCREEN_WIDTH / 4, 20))

    pygame.display.update()
    clock.tick(FPS)