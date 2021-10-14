"""
Tic Tac Toe for 1 or 2 polayers, implementing an opponent with A.I. (using Minimax)
Marco Coria, 2021
"""

from sys import exit
from random import randint
import pygame
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

clock = pygame.time.Clock()

# Pygame main screen
screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
pygame.display.set_caption( 'Tic Tac Toe' )
game_icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(game_icon)

# Game board
tiles_surfaces = [[pygame.Surface( (150,150) ) for _ in range(3)] for _ in range(3)]
tiles_coord = [
    [(0,0), (150,0), (300,0)],
    [(0,150), (150,150), (300,150)],
    [(0,300), (150,300), (300,300)],
]
tiles_rects = [[tiles_surfaces[i][j].get_rect() for j in range(3)] for i in range(3)]

# Game log / buttons
config_toggle_surf = pygame.Surface( (130, 46) )
config_toggle_rect = config_toggle_surf.get_rect( bottomright=(WINDOW_WIDTH - 3, WINDOW_HEIGHT - 53) )

reset_toggle_surf = pygame.Surface( (130, 46) )
reset_toggle_rect = reset_toggle_surf.get_rect( bottomright=(WINDOW_WIDTH - 3, WINDOW_HEIGHT - 10) )

ingame_font = pygame.font.Font('assets/Pixeltype.ttf', 40)

# Config screen
config_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
config_bg_rect = config_bg.get_rect(topleft=(0,0))
config_panel = pygame.Surface((WINDOW_WIDTH - 30, WINDOW_HEIGHT - 150))
config_panel_rect = config_panel.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

DBUTTON_HEIGHT = WINDOW_HEIGHT/4
DBUTTON_WIDTH = (WINDOW_WIDTH-40)/8
difficulty_surfaces = [pygame.Surface( (90,50) ) for _ in range(4)]
for ds in difficulty_surfaces: ds.set_alpha((100))
difficulty_rects = [
    difficulty_surfaces[0].get_rect(center=(DBUTTON_WIDTH + 20, DBUTTON_HEIGHT + 200)),
    difficulty_surfaces[1].get_rect(center=(DBUTTON_WIDTH * 3 + 20, DBUTTON_HEIGHT + 200)),
    difficulty_surfaces[2].get_rect(center=(DBUTTON_WIDTH * 5 + 20, DBUTTON_HEIGHT + 200)),
    difficulty_surfaces[3].get_rect(center=(DBUTTON_WIDTH * 7 + 20, DBUTTON_HEIGHT + 200)),
]
difficulty_colors = [
    '#3eb33e',
    '#b39d3e',
    '#b0653a',
    '#ba332f',
]

EBUTTON_HEIGHT = DBUTTON_HEIGHT
EBUTTON_WIDTH = (WINDOW_WIDTH-40) / 4
players_surfaces = [pygame.Surface( (185, 50) ) for _ in range(2)]
players_rects = [
    players_surfaces[0].get_rect(center=(EBUTTON_WIDTH + 20, EBUTTON_HEIGHT + 50)),
    players_surfaces[0].get_rect(center=(EBUTTON_WIDTH * 3 + 20, EBUTTON_HEIGHT + 50)),
]

ebutton_font = pygame.font.Font('assets/Pixeltype.ttf', 40)
eselection_surfaces = [
    ebutton_font.render('1 vs 1', True, '#fafafa'),
    ebutton_font.render('1 vs CPU', True, '#fafafa')
]
eselection_rects = [
    eselection_surfaces[i].get_rect(center=(185/2,54/2)) for i in range(2)
]

players_colors = [
    '#2260ab',
    '#8422ab'
]

title_font = pygame.font.Font('assets/Pixeltype.ttf', 60)

dtitle_surface = title_font.render('Dificultad', True, '#fafafa')
dtitle_surface.set_alpha(100)
dtitle_rect = dtitle_surface.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

etitle_surface = title_font.render('Modo', True, '#fafafa')
etitle_rect = etitle_surface.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 150))

button_font = pygame.font.Font('assets/Pixeltype.ttf', 45)

accept_surface = button_font.render('Aceptar', True, '#fafafa')
accept_rect = accept_surface.get_rect(center=(WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2 + 150))

cancel_surface = button_font.render('Cancelar', True, '#fafafa')
cancel_rect = cancel_surface.get_rect(center=(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 150))

log_font = pygame.font.Font('assets/Pixeltype.ttf', 45)

def get_tile_clicked(mouse_pos):
    """
    Returns the tile of the board where is located the cursor
    """
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
    else:
        tile = None

    return tile

def main():
    """
    Main game loop
    """

    # Game initial config
    LIMIT_H = 4 # Minimax tree max depth (aka. Difficulty)
    players = 1
    game_active = True
    player_turn = True if randint(0,1) == 1 else False
    last_start = player_turn
    winner = 0
    last = 0
    cooldown = 600
    board = [[0 for _ in range(3)] for _ in range(3)]

    # Minimax Agent
    agent_player = None

    # Config variables
    config_active = False
    difficulty_selected = False
    players_selected = False

    while True:
        if not players_selected: selected_players = 0

        # PC Player (Minimax Agent)
        if players == 1 and game_active and not player_turn:
            cooldown = randint(300,1200)
            now = pygame.time.get_ticks()
            if now - last >= cooldown:
                if agent_player == None:
                    agent_player = Agent(board, LIMIT_H)
                board = agent_player.move(board)
                player_turn = True

        # User events
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Toggle Config panel (key)
                if event.key == pygame.K_c:
                    if config_active:
                        selected = LIMIT_H
                        difficulty_selected = False
                        players_selected = False
                        accept_surface.set_alpha(100)
                        dtitle_surface.set_alpha(100)
                        for difficulty_surface in difficulty_surfaces:
                            difficulty_surface.set_alpha(100)
                        for players_surface in players_surfaces:
                            players_surface.set_alpha(255)
                    game_active = not game_active
                    config_active = not config_active
                # Reset Game (key)
                if event.key == pygame.K_r:
                    game_active = True
                    player_turn = not last_start
                    last_start = player_turn
                    agent_player = None
                    winner = 0
                    board = [[0 for _ in range(3)] for _ in range(3)]
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Reset Game (ingame button)
                if reset_toggle_rect.collidepoint(pygame.mouse.get_pos()) and not config_active:
                    game_active = True
                    player_turn = not last_start
                    last_start = player_turn
                    agent_player = None
                    winner = 0
                    board = [[0 for _ in range(3)] for _ in range(3)]
                # Toggle Config panel (ingame button)
                if config_toggle_rect.collidepoint(pygame.mouse.get_pos()) and not config_active:
                    game_active = not game_active
                    config_active = not config_active
                if game_active:
                    # User move
                    mouse_pos = pygame.mouse.get_pos()
                    tile = get_tile_clicked(mouse_pos)
                    last = pygame.time.get_ticks()

                    if tile != None:
                        if board[tile[0]][tile[1]] == 0:
                            if player_turn: board[tile[0]][tile[1]] = 1 # Player 1
                            elif players == 2: board[tile[0]][tile[1]] = 2 # Player 2 (if active)
                            player_turn = not player_turn

                            # Minimax tree state update (if active)
                            if players == 1:
                                if agent_player == None:
                                    agent_player = Agent(board, LIMIT_H)
                                agent_player.check_usermov(board)
                else:
                    # Config events
                    if config_active:
                        if not difficulty_selected: selected = LIMIT_H
                        # Dismiss Config panel (click outside or Cancel button)
                        if config_bg_rect.collidepoint(pygame.mouse.get_pos()) and not config_panel_rect.collidepoint(pygame.mouse.get_pos()) or cancel_rect.collidepoint(pygame.mouse.get_pos()):
                            config_active = not config_active
                            game_active = not game_active
                            selected = LIMIT_H
                            difficulty_selected = False
                            players_selected = False
                            accept_surface.set_alpha(100)
                            dtitle_surface.set_alpha(100)
                            for difficulty_surface in difficulty_surfaces:
                                difficulty_surface.set_alpha(100)
                            for players_surface in players_surfaces:
                                players_surface.set_alpha(255)
                        else:
                            # Difficulty selector
                            for i, difficulty_rect in enumerate(difficulty_rects):
                                if difficulty_rect.collidepoint(pygame.mouse.get_pos()) and selected_players == 1:
                                    difficulty_selected = True
                                    selected = (i + 1) * 2

                                    accept_surface.set_alpha(255)
                                    for j, difficulty_rect in enumerate(difficulty_rects):
                                        if i == j and selected_players == 1: difficulty_surfaces[j].set_alpha(255)
                                        else: difficulty_surfaces[j].set_alpha(100)

                            # Players selector
                            for i, players_rect in enumerate(players_rects):
                                if players_rect.collidepoint(pygame.mouse.get_pos()):
                                    players_selected = True
                                    if i == 0:
                                        selected_players = 2
                                        difficulty_selected = False
                                        dtitle_surface.set_alpha(100)
                                        for difficulty_surface in difficulty_surfaces:
                                            difficulty_surface.set_alpha(100)
                                    else:
                                        selected_players = 1
                                        if difficulty_selected == False:
                                            dtitle_surface.set_alpha(255)
                                            for difficulty_surface in difficulty_surfaces:
                                                difficulty_surface.set_alpha(255)
                                        

                                    for j, players_rect in enumerate(players_rects):
                                        if i == j: players_surfaces[j].set_alpha(255)
                                        else: players_surfaces[j].set_alpha(100)
                            
                            # Accept config event (resets entire game)
                            if accept_rect.collidepoint(pygame.mouse.get_pos()) and (difficulty_selected or selected_players == 2):
                                game_active = True
                                config_active = False
                                player_turn = last_start
                                agent_player = None
                                winner = 0
                                board = [[0 for _ in range(3)] for _ in range(3)]
                                if difficulty_selected: LIMIT_H = selected
                                players = selected_players
                                selected = LIMIT_H
                                difficulty_selected = False
                                players_selected = False
                                accept_surface.set_alpha(100)
                                dtitle_surface.set_alpha(100)
                                for difficulty_surface in difficulty_surfaces:
                                    difficulty_surface.set_alpha(100)
                                for players_surface in players_surfaces:
                                    players_surface.set_alpha(255)

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

        config_toggle_surf.fill('#cc9349')
        ct_surface = ingame_font.render('Config', True, '#fafafa')
        ct_rect = ct_surface.get_rect( center=(130/2, 46/2) )
        config_toggle_surf.blit(ct_surface, ct_rect)
        screen.blit(config_toggle_surf, config_toggle_rect)

        reset_toggle_surf.fill('#cc9349')
        rt_surface = ingame_font.render('Reset', True, '#fafafa')
        rt_rect = rt_surface.get_rect( center=(130/2, 46/2) )
        reset_toggle_surf.blit(rt_surface, rt_rect)
        screen.blit(reset_toggle_surf, reset_toggle_rect)

        pygame.draw.rect( screen, '#d67631', config_toggle_rect, width=3)
        pygame.draw.rect( screen, '#d67631', reset_toggle_rect, width=3)

        if player_turn:
            if players == 1:
                if winner == 0: turn_surface = button_font.render('Turno: Jugador', True, '#fafafa')
                else: turn_surface = button_font.render('Ganador: PC!', True, '#fafafa')
            else: 
                if winner == 0: turn_surface = button_font.render('Turno: Jugador 1', True, '#fafafa')
                else: turn_surface = button_font.render('Ganador: Jugador 2!', True, '#fafafa')
        else:
            if players == 1:
                if winner == 0: turn_surface = button_font.render('Turno: PC', True, '#fafafa')
                else: turn_surface = button_font.render('Ganador: Jugador!', True, '#fafafa')
            else:
                if winner == 0: turn_surface = button_font.render('Turno: Jugador 2', True, '#fafafa')
                else: turn_surface = button_font.render('Ganador: Jugador 1!', True, '#fafafa')
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
            screen.blit(etitle_surface, etitle_rect)

            for i, difficulty_surface in enumerate(difficulty_surfaces):
                difficulty_surface.fill(difficulty_colors[i])
                screen.blit(difficulty_surface, difficulty_rects[i])
            
            for i, players_surface in enumerate(players_surfaces):
                players_surface.fill(players_colors[i])
                players_surface.blit(eselection_surfaces[i], eselection_rects[i])
                screen.blit(players_surface, players_rects[i])

            if (difficulty_selected and selected_players == 1) or selected_players == 2:
                accept_surface.set_alpha(255)
            else:
                accept_surface.set_alpha(100)
            screen.blit(accept_surface, accept_rect)
            screen.blit(cancel_surface, cancel_rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()