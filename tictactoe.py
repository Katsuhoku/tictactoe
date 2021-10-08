"""
Tic Tac Toe with Minimax opponents
"""

from sys import exit
import pygame
from random import randint
from agent import Agent

# --- CONSTANTS --- #
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 550

BACKGROUND = '#14bdac'
LOG_BACKGROUND = '#242424'
LINE_COLOR = '#0da192'
PLAYER_COLORS = [
    '#f2ebd3',
    '#545454'
]

winning_sequences = [
    [(0,0),(0,1),(0,2)],
    [(1,0),(1,1),(1,2)],
    [(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)],
    [(0,1),(1,1),(2,1)],
    [(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)],
    [(0,2),(1,1),(2,0)]
]

start_end_points = [
    [(0,75),(450,75)],
    [(0,225),(450,225)],
    [(0,375),(450,375)],
    [(75,0),(75,450)],
    [(225,0),(225,450)],
    [(375,0),(375,450)],
    [(0,0),(450,450)],
    [(450,0),(0,450)],
]

# --- PYGAME CONFIG --- #

pygame.init()
screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
pygame.display.set_caption( 'Tic Tac Toe' )

clock = pygame.time.Clock()

tiles_surfaces = [[pygame.Surface( (150,150) ) for _ in range(3)] for _ in range(3)]
tiles_coord = [
    [(0,0), (150,0), (300,0)],
    [(0,150), (150,150), (300,150)],
    [(0,300), (150,300), (300,300)],
]
tiles_rects = [[tiles_surfaces[i][j].get_rect() for j in range(3)] for i in range(3)]

# Config screen
config_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
config_bg_rect = config_bg.get_rect(topleft=(0,0))
config_panel = pygame.Surface((WINDOW_WIDTH - 30, WINDOW_HEIGHT - 300))
config_panel_rect = config_panel.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

difficulty_surfaces = [pygame.Surface( (110,50) ) for _ in range(3)]
difficulty_rects = [
    difficulty_surfaces[0].get_rect(center=(WINDOW_WIDTH/2 - 120, WINDOW_HEIGHT/2)),
    difficulty_surfaces[1].get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)),
    difficulty_surfaces[2].get_rect(center=(WINDOW_WIDTH/2 + 120, WINDOW_HEIGHT/2)),
]
difficulty_colors = [
    '#3eb33e',
    '#b39d3e',
    '#b3423e'
]

dtitle_font = pygame.font.Font('assets/Pixeltype.ttf', 60)
dtitle_surface = dtitle_font.render('Dificultad', True, '#fafafa')
dtitle_rect = dtitle_surface.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 70))

button_font = pygame.font.Font('assets/Pixeltype.ttf', 45)

accept_surface = button_font.render('Aceptar', True, '#fafafa')
accept_rect = accept_surface.get_rect(center=(WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2 + 70))

cancel_surface = button_font.render('Cancelar', True, '#fafafa')
cancel_rect = cancel_surface.get_rect(center=(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 70))

log_font = pygame.font.Font('assets/Pixeltype.ttf', 45)

def get_tile_clicked(mouse_pos):
    tile = [0,0] # tile clicked
    if 0 <= mouse_pos[0] < 150:
        tile[1] = 0 # Left column
    elif mouse_pos[0] < 300:
        tile[1] = 1 # Center column
    elif mouse_pos[0] <= 450:
        tile[1] = 2 # Right column

    if 0 <= mouse_pos[1] < 150:
        tile[0] = 0 # Top row
    elif mouse_pos[1] < 300:
        tile[0] = 1 # Center row
    elif mouse_pos[1] <= 450:
        tile[0] = 2 # Bottom row

    return tile

def main():
    LIMIT_H = 6
    game_active = True
    config_active = False
    difficulty_selected = False
    player_turn = True if randint(0,1) == 1 else False
    last_start = player_turn
    winner = 0
    cooldown = 600
    last = 0


    board = [
        [0,0,0],
        [0,0,0],
        [0,0,0],
    ]

    agent_player = None

    while True:
        # PC
        if game_active and not player_turn:
            now = pygame.time.get_ticks()
            if now - last >= cooldown:
                if agent_player == None:
                    agent_player = Agent(board, LIMIT_H)
                board = agent_player.move(board)
                player_turn = True

        # User events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if config_active:
                        selected = LIMIT_H
                        difficulty_selected = False
                        accept_surface.set_alpha(100)
                        for difficulty_surface in difficulty_surfaces:
                            difficulty_surface.set_alpha(255)
                    game_active = not game_active
                    config_active = not config_active
                if event.key == pygame.K_r: # Reset game
                    game_active = True
                    player_turn = not last_start
                    last_start = player_turn
                    agent_player = None
                    winner = 0
                    board = [
                        [0,0,0],
                        [0,0,0],
                        [0,0,0],
                    ]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_active:
                    if player_turn:
                        mouse_pos = pygame.mouse.get_pos()
                        tile = get_tile_clicked(mouse_pos)
                        last = pygame.time.get_ticks()

                        if board[tile[0]][tile[1]] == 0:
                            board[tile[0]][tile[1]] = 1
                            player_turn = False
                            if agent_player == None:
                                agent_player = Agent(board, LIMIT_H)
                            agent_player.check_usermov(board)
                else:
                    if config_active:
                        if not difficulty_selected: selected = LIMIT_H
                        if config_bg_rect.collidepoint(pygame.mouse.get_pos()) and not config_panel_rect.collidepoint(pygame.mouse.get_pos()) or cancel_rect.collidepoint(pygame.mouse.get_pos()):
                            config_active = not config_active
                            game_active = not game_active
                            selected = LIMIT_H
                            difficulty_selected = False
                            accept_surface.set_alpha(100)
                            for difficulty_surface in difficulty_surfaces:
                                difficulty_surface.set_alpha(255)
                        else:
                            for i, difficulty_rect in enumerate(difficulty_rects):
                                if difficulty_rect.collidepoint(pygame.mouse.get_pos()):
                                    difficulty_selected = True
                                    accept_surface.set_alpha(255)

                                    difficulty_surfaces[i].set_alpha(255)
                                    difficulty_surfaces[i-1].set_alpha(100)
                                    difficulty_surfaces[(i+1)%3].set_alpha(100)

                                    if i == 0: selected = 2
                                    if i == 1: selected = 4
                                    if i == 2: selected = 6
                            
                            if accept_rect.collidepoint(pygame.mouse.get_pos()) and difficulty_selected: # Reset Game
                                game_active = True
                                config_active = False
                                player_turn = last_start
                                agent_player = None
                                winner = 0
                                board = [
                                    [0,0,0],
                                    [0,0,0],
                                    [0,0,0],
                                ]
                                LIMIT_H = selected
                                selected = LIMIT_H
                                difficulty_selected = False
                                accept_surface.set_alpha(100)
                                for difficulty_surface in difficulty_surfaces:
                                    difficulty_surface.set_alpha(255)

        # Game window (board/log)
        screen.fill(LOG_BACKGROUND)
        for i, tile_row in enumerate(tiles_surfaces):
            for j, tile_surface in enumerate(tile_row):
                tile_surface.fill(BACKGROUND)
                if board[i][j] == 1:
                    pygame.draw.circle( tile_surface, PLAYER_COLORS[0], tiles_rects[i][j].center, (tiles_rects[i][j].bottom - 30) /2, width=15 )
                elif board[i][j] == 2:
                    pygame.draw.line( tile_surface, PLAYER_COLORS[1], (30,30), (120,120), width=20 )
                    pygame.draw.line( tile_surface, PLAYER_COLORS[1], (30,120), (120,30), width=20 )

                screen.blit( tile_surface, tiles_coord[i][j] )

        pygame.draw.line( screen, LINE_COLOR, (150,0), (150,450), 7 )
        pygame.draw.line( screen, LINE_COLOR, (300,0), (300,450), 7 )
        pygame.draw.line( screen, LINE_COLOR, (0,150), (450,150), 7 )
        pygame.draw.line( screen, LINE_COLOR, (0,300), (450,300), 7 )



        if player_turn:
            turn_surface = button_font.render('Turno: Jugador', True, '#fafafa')
        else:
            turn_surface = button_font.render('Turno: PC', True, '#fafafa')
        turn_rect = cancel_surface.get_rect(midleft=(20, WINDOW_HEIGHT - 50))
        screen.blit(turn_surface, turn_rect)

        # Check for winner
        if game_active:
            game_active = False
            for row in board:
                if 0 in row:
                    game_active = True
                    break

            for w, ws in enumerate(winning_sequences):
                if board[ws[0][0]][ws[0][1]] == 1 and board[ws[1][0]][ws[1][1]] == 1 and board[ws[2][0]][ws[2][1]] == 1:
                    winner = 1
                    line = w
                    game_active = False
                    break
                if board[ws[0][0]][ws[0][1]] == 2 and board[ws[1][0]][ws[1][1]] == 2 and board[ws[2][0]][ws[2][1]] == 2:
                    winner = 2
                    line = w
                    game_active = False
                    break
            

        if winner != 0:
            pygame.draw.line( screen, PLAYER_COLORS[winner-1], start_end_points[line][0], start_end_points[line][1], width=15 )
        
        # Config Window
        if config_active:
            config_bg.set_alpha(200)
            config_bg.fill('Black')
            screen.blit(config_bg, config_bg_rect)

            config_panel.fill('#222423')
            screen.blit(config_panel, config_panel_rect)
            
            screen.blit(dtitle_surface, dtitle_rect)

            for i, difficulty_surface in enumerate(difficulty_surfaces):
                difficulty_surface.fill(difficulty_colors[i])
                screen.blit(difficulty_surface, difficulty_rects[i])

            if not difficulty_selected:
                accept_surface.set_alpha(100)
            screen.blit(accept_surface, accept_rect)
            screen.blit(cancel_surface, cancel_rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()