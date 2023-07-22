import pygame
import random
import time
import math

pygame.init()

cell_size = 10  # Size of each grid cell

width = 800
height = 800

# determines the density of the grid (higher = less dense)
resolution = 10

cols = width // resolution
rows = height // resolution

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("John Conway's Game of Life")

'''
TODO: make a start menu with options to choose from such as
- select the resolution.
- set the screen size.
- allow the ability to change the speed on the fly.
'''

def main():
    grid = createGrid(cols, rows)
    next_grid = createGrid(cols, rows)
    
    left_dragging = False
    right_dragging = False
    draw_grid = True
    
    paused = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                
                if event.key == pygame.K_BACKSPACE:
                    for x in range(len(grid)):
                        for y in range(len(grid[0])):
                            grid[x][y] = 0
                # the 'g' key is being pressed
                if event.key == 103:
                    draw_grid = not draw_grid
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_dragging = True
                elif event.button == 3:
                    right_dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_dragging = False
                elif event.button == 3:
                    right_dragging = False

        if left_dragging or right_dragging:
            mx, my = pygame.mouse.get_pos()
            mx //= resolution
            my //= resolution
            
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if mx == x and my == y and left_dragging:
                        grid[x][y] = 1
                    if mx == x and my == y and right_dragging:
                        grid[x][y] = 0
        
        screen.fill((255, 255, 255))
            
        next_grid = createGrid(cols, rows)
        
        # draw all the alive squares on the screen
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (y * resolution, x * resolution, resolution, resolution))
                if grid[y][x] == 3:
                    pygame.draw.rect(screen, (0, 255, 0), (y * resolution, x * resolution, resolution, resolution))
                
        # draw the grid lines
        if draw_grid:
            for x in range(0, width, resolution):
                for y in range(0, height, resolution):
                    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, height))

                    pygame.draw.line(screen, (50, 50, 50), (0, y), (width, y))
        
        # compute
        if not paused:
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    state = grid[x][y]
                    neighbors = checkNeighbors(grid, x, y)
                    
                    if state == 0 and neighbors == 3:
                        next_grid[x][y] = 1;
                    elif state == 1 and neighbors < 2 or neighbors > 3:
                        next_grid[x][y] = 0;
                    else:
                        next_grid[x][y] = state
                        
            grid = next_grid
                     
        pygame.display.flip()
    pygame.quit()

def checkNeighbors(grid: list, x, y):
    neighbors = 0
    
    for dirX in [-1, 0, 1]:
        for dirY in [-1, 0, 1]:
            col = (x + dirX + cols) % cols
            row = (y + dirY + rows) % rows
            
            neighbors += grid[col][row]
    
    # take away ourselves, kind of janky
    neighbors -= grid[x][y]
    return neighbors

def createGrid(cols, rows, addRandom = False):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    alive = 0
    
    if addRandom:
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                rand_num = random.randint(0, 1)
                grid[x][y] = rand_num
    
    return grid

main()