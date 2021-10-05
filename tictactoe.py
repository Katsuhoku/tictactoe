"""
Tic Tac Toe with Minimax opponents
"""

from sys import exit
import pygame
from random import randint
#from minimax import agent

LIMIT_H = 4

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 450

BACKGROUND = '#14bdac'
WINNER_BACKGROUND = '#1ac734'
LINE_COLOR = '#0da192'
PLAYER_COLORS = [
    '#f2ebd3',
    '#545454'
]

pygame.init()
screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
pygame.display.set_caption( 'Tic Tac Toe' )

game_active = True
player_turn = True

clock = pygame.time.Clock()

board = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
]

tiles_surfaces = [[pygame.Surface( (150,150) ) for _ in range(3)] for _ in range(3)]
tiles_coord = [
    [(0,0), (150,0), (300,0)],
    [(0,150), (150,150), (300,150)],
    [(0,300), (150,300), (300,300)],
]
tiles_rects = [[tiles_surfaces[i][j].get_rect() for j in range(3)] for i in range(3)]

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

winner = 0

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
    global game_active
    global player_turn
    global board
    global winner
    cooldown = 180
    last = 0

    while True:
        # PC
        if game_active and not player_turn:
            # try:
            #     agent_player
            # except NameError:
            #     agent_player = agent.Agent(board, LIMIT_H)
            # agent_tile = agent_player.move(board)

            # board[agent_tile[0]][agent_tile[1]] = 2
            # player_turn = True

            now = pygame.time.get_ticks()
            if now - last >= cooldown:
                i, j = randint(0, 2), randint(0, 2)
                while board[i][j] != 0:
                    i, j = randint(0, 2), randint(0, 2)
                board[i][j] = 2
                player_turn = True

        # User events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Reset game
                    game_active = True
                    player_turn = True
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
                    # else:
                    #     mouse_pos = pygame.mouse.get_pos()
                    #     tile = get_tile_clicked(mouse_pos)

                    #     if board[tile[0]][tile[1]] == 0:
                    #         board[tile[0]][tile[1]] = 2
                    #         player_turn = not player_turn

        # Game window (board/log)
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

        # Check for winner
        if game_active:
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

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()