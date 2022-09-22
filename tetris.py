import pygame
import random
from Piece import Piece
from pygame.locals import *

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


# We will loop through these locked positions and modify our blank grid to show these pieces
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):

            if (j, i) in locked_positions:
                temp = locked_positions[(j, i)]
                grid[i][j] = temp

    return grid

# Converting the shape form
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        
        for j, column in enumerate(row):
            
            if column == '0':
                positions.append((shape.x + j, shape.y + i))   
                
    """ for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) """
    
    return positions


# Checking the valid space according to the color ((0,0,0) is mean that it is empty)
def valid_space(shape, grid):
    accepted_positions = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)
    
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    
    return True

# If the player reached the top of the screen, then game is over 
def check_lost(positions):
    for pos in positions:
        x,y = pos
        
        if y < 1:
            return True
    
    return False


# Get the random shape
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes), shape_colors, shapes)


def draw_text_middle(text, size, color, surface):
    pass

# This function draws the grey grid lines that we see
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    
    for i in range(len(grid)):
        # Horizontal lines
        pygame.draw.line(surface, (128,128,128), (sx, sy + i * 30), (sx + play_width, sy + i * 30))

    for j in range(len(grid[i])):
        # Vertical lines
        pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))

def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface,grid):
    surface.fill((0, 0, 0))

    # Tetris title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width /
                 2 - (label.get_width() / 2), 30))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):

            pygame.draw.rect(
                surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    pygame.draw.rect(surface,(255,0,0), (top_left_x,top_left_y,play_width,play_height), 5)

    # draw grid and border
    draw_grid(surface, grid)
    pygame.display.update()


def main(surface):
    global grid
    
    locked_positions = {}  # (x,y) : (255,0,0)
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    
    while run:
        # Variables
        fall_speed = 0.27
        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        
        # Piece is falling code
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run == False
                pygame.display.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                # Going left
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    # If there is no space for going left, keep going to the current direction
                    if not valid_space(current_piece,grid):
                        current_piece.x += 1
                
                # Going right
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    # If there is no space for going right, keep going to the current direction
                    if not valid_space(current_piece,grid):
                        current_piece.x -= 1
                        
                # Rotating
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)  

                if event.key == pygame.K_DOWN:
                    # Move shape down
                    current_piece.y += 1
                    
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
        
        shape_pos = convert_shape_format(current_piece)
        
        # add color of piece to the grid for drawing
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            
            # If we are not above the screen
            if y > -1:
                grid[y][x] = current_piece.color

        # If piece hit ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0],pos[1])
                locked_positions[p] = current_piece.color
            
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            
        draw_window(surface,grid)


def main_menu(surface):
    main(surface)

surface = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(surface)  # start game
