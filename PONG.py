import pygame, sys, random
from pygame.locals import *

pygame.init()
main_clock = pygame.time.Clock()

WINDOWWIDTH = 1000
WINDOWHEIGHT = 500
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('PONG')

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

player1 = pygame.Rect(WINDOWWIDTH - 20 , WINDOWHEIGHT/2 - 50, 20, 100)
player2 = pygame.Rect(0, WINDOWHEIGHT/2 - 50, 20, 100)

move_up1 = False
move_down1 = False

move_up2 = False
move_down2 = False

score1 = 0
score2 = 0
SCORE_TO_WIN = 3

MOVESPEED_p = 5
MOVESPEED_b = 5

DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'

MOVES = [DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT]

out_of_the_window = False
pause = False
previous_direction = ''

b1 = {'rect':pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 30, 30),
      'color':RED,
      'dir':UPRIGHT}

basic_font = pygame.font.SysFont(None, 48)

text1 = basic_font.render(f'Score: {score2}', True, BLACK)
text_rect1 = text1.get_rect()

text_rect1.centerx = window_surface.get_rect().left + 80
text_rect1.centery = window_surface.get_rect().bottom - 30

text2 = basic_font.render(f'Score: {score1}', True, BLACK)
text_rect2 = text2.get_rect()
text_rect2.centerx = window_surface.get_rect().right - 100
text_rect2.centery = window_surface.get_rect().bottom - 30

winning_message = '                 '

text3 = basic_font.render(winning_message, True, BLACK)
text_rect3 = text3.get_rect()
text_rect3.centerx = window_surface.get_rect().centerx - text_rect3.width/2
text_rect3.centery = window_surface.get_rect().centery - text_rect3.height*2

move_left1 = False
move_right1 = False


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                move_down1 = False
                move_up1 = True
            if event.key == K_DOWN:
                move_up1 = False
                move_down1 = True

            if event.key == K_SPACE:
                if pause == True:
                    pause = False
                    b1['dir'] = previous_direction
                    out_of_the_window = False
                    winning_message = ''
                else:
                    pause = True
                    b1['dir'] = 0

            if event.key == K_w:
                move_down2 = False
                move_up2 = True
            if event.key == K_s:
                move_up2 = False
                move_down2 = True

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_UP:
                move_up1 = False
            if event.key == K_DOWN:
                move_down1 = False

            if event.key == K_w:
                move_up2 = False
            if event.key == K_s:
                move_down2 = False

    window_surface.fill(WHITE)

    if b1['dir'] == DOWNLEFT:
        b1['rect'].centerx -= MOVESPEED_b
        b1['rect'].centery += MOVESPEED_b
        previous_direction = b1['dir']
    if b1['dir'] == DOWNRIGHT:
        b1['rect'].centerx += MOVESPEED_b
        b1['rect'].centery += MOVESPEED_b
        previous_direction = b1['dir']
    if b1['dir'] == UPLEFT:
        b1['rect'].centerx -= MOVESPEED_b
        b1['rect'].centery -= MOVESPEED_b
        previous_direction = b1['dir']
    if b1['dir'] == UPRIGHT:
        b1['rect'].centerx += MOVESPEED_b
        b1['rect'].centery -= MOVESPEED_b
        previous_direction = b1['dir']

    if b1['rect'].top < 0:
        if b1['dir'] == UPLEFT:
            b1['dir'] = DOWNLEFT
        if b1['dir'] == UPRIGHT:
            b1['dir'] = DOWNRIGHT
    if b1['rect'].bottom > WINDOWHEIGHT:
        if b1['dir'] == DOWNLEFT:
            b1['dir'] = UPLEFT
        if b1['dir'] == DOWNRIGHT:
            b1['dir'] = UPRIGHT
    if b1['rect'].left < 0:
        b1['dir'] = MOVES[random.randint(0,3)]
        score1 += 1
        out_of_the_window = True
        MOVESPEED_b = 5
    if b1['rect'].right > WINDOWWIDTH:
        b1['dir'] = MOVES[random.randint(0,3)]
        score2 += 1
        out_of_the_window = True
        MOVESPEED_b = 5

    pygame.draw.circle(window_surface, b1['color'], (b1['rect'].centerx, b1['rect'].centery), 20)

    if out_of_the_window:
        b1['rect'].centerx = window_surface.get_rect().centerx - b1['rect'].width/2
        b1['rect'].centery = window_surface.get_rect().centery - b1['rect'].height/2
        player2 = pygame.Rect(0, WINDOWHEIGHT/2 - 100/2, 20, 100)
        player1 = pygame.Rect(WINDOWWIDTH - player1.width, WINDOWHEIGHT/2 - player1.height/2, 20, 100)
        pause = True

    if score1 > score2 and score1 == SCORE_TO_WIN:
        winning_message = 'Player 1 has WON!'
        pause = True
        score1 = 0
        score2 = 0
    if score1 < score2 and score2 == SCORE_TO_WIN:
        winning_message = 'Player 2 has WON!'
        pause = True
        score1 = 0
        score2 = 0

    window_surface.blit(text3, text_rect3)
    text3 = basic_font.render(winning_message, True, BLACK)

    player1 = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
    pygame.draw.rect(window_surface, BLACK, player1)
    player2 = pygame.Rect(player2.x, player2.y, player2.width, player2.height)
    pygame.draw.rect(window_surface, BLUE, player2)

    if move_down1 and player1.bottom < WINDOWHEIGHT and not pause:
        player1.bottom += MOVESPEED_p
    if move_up1 and player1.top > 0 and not pause:
        player1.top -= MOVESPEED_p

    if move_left1 and player1.left > 0 and not pause:
        player1.left -= MOVESPEED_p
    if move_right1 and player1.right < WINDOWWIDTH and not pause:
        player1.right += MOVESPEED_p

    if move_down2 and player2.bottom < WINDOWHEIGHT and not pause:
        player2.bottom += MOVESPEED_p
    if move_up2 and player2.top > 0 and not pause:
        player2.top -= MOVESPEED_p


    if player1.colliderect(b1['rect']):
        if b1['dir'] == DOWNRIGHT:
            b1['dir'] = DOWNLEFT
        if b1['dir'] == UPRIGHT:
            b1['dir'] = UPLEFT

        MOVESPEED_b += 0.5

    if player2.colliderect(b1['rect']):
        if b1['dir'] == DOWNLEFT:
            b1['dir'] = DOWNRIGHT
        if b1['dir'] == UPLEFT:
            b1['dir'] = UPRIGHT

        MOVESPEED_b += 0.5

    window_surface.blit(text1, text_rect1)
    text1 = basic_font.render(f'Score: {score2}', True, BLACK)
    window_surface.blit(text2, text_rect2)
    text2 = basic_font.render(f'Score: {score1}', True, BLACK)

    pygame.display.update()
    main_clock.tick(65)
