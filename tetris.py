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
                temp = locked_positions[(i, j)]
                grid[i][j] = temp

    return grid


def convert_shape_format(shape):
    pass


def valid_space(shape, grid):
    pass


def check_lost(positions):
    pass

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
        pygame.draw.line(surface, (128,128,128), (sx, sy + i *30), (sx + play_width, sy + i * 30))

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
    
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    
    while run:
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
        draw_window(surface,grid)


def main_menu(surface):
    main(surface)

surface = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(surface)  # start game
