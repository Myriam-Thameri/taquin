import os
from turtledemo import clock
import threading
import random
import pygame
from taquin import transition
from taquin import liste as l
from taquin import recherche_dfs, recherche_dfs_limite
from taquin import goal
import taquin
from taquin import etat_final
import sys

WIDTH, HEIGHT = 550, 300
TILE_SIZE = 300 // 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

button_width = 100
button_height = 50
button_margin = 20


def shuffle_liste():
    initial_state = list(range(9))
    liste = []
    random.shuffle(initial_state)
    for i in range(0, 9, 3):
        row = initial_state[i:i + 3]
        liste.append(row)
    return liste


def load_number_images():
    number_images = {}
    number_images[0] = pygame.image.load(os.path.join('png', 'R.jpg'))
    number_images[1] = pygame.image.load(os.path.join('png', '001-number-1.png'))
    number_images[2] = pygame.image.load(os.path.join('png', '002-number-2.png'))
    number_images[4] = pygame.image.load(os.path.join('png', '003-number-4.png'))
    number_images[5] = pygame.image.load(os.path.join('png', '004-number-5.png'))
    number_images[3] = pygame.image.load(os.path.join('png', '005-number-3.png'))
    number_images[6] = pygame.image.load(os.path.join('png', '006-number-6.png'))
    number_images[7] = pygame.image.load(os.path.join('png', '007-number-7.png'))
    number_images[8] = pygame.image.load(os.path.join('png', '008-number-8.png'))
    return number_images


def draw_grid(screen):
    for x in range(0, 300, TILE_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (300, y))


def draw_tiles(screen, liste, number_images):
    for i in range(3):
        for j in range(3):
            value = liste[i][j]
            image = number_images[value]
            cell_x = j * TILE_SIZE
            cell_y = i * TILE_SIZE
            image_x = cell_x + (TILE_SIZE - image.get_width()) // 2
            image_y = cell_y + (TILE_SIZE - image.get_height()) // 2
            screen.blit(image, (image_x, image_y))


def move_tile(puzzle, next_state):
    empty_index = None
    new_index = None

    for i, row in enumerate(puzzle):
        if 0 in row:
            empty_index = [i, row.index(0)]
            break

    for i, row in enumerate(next_state):
        if 0 in row:
            new_index = [i, row.index(0)]
            break
    dx = new_index[0] - empty_index[0]
    dy = new_index[1] - empty_index[1]

    if dx == 0 and dy == 1:
        puzzle[empty_index[0]][empty_index[1]], puzzle[empty_index[0]][empty_index[1] + 1] = puzzle[empty_index[0]][
            empty_index[1] + 1], puzzle[empty_index[0]][empty_index[1]]
    elif dx == 0 and dy == -1:
        puzzle[empty_index[0]][empty_index[1]], puzzle[empty_index[0]][empty_index[1] - 1] = puzzle[empty_index[0]][
            empty_index[1] - 1], puzzle[empty_index[0]][empty_index[1]]
    elif dx == 1 and dy == 0:
        puzzle[empty_index[0]][empty_index[1]], puzzle[empty_index[0] + 1][empty_index[1]] = puzzle[empty_index[0] + 1][
            empty_index[1]], puzzle[empty_index[0]][empty_index[1]]
    elif dx == -1 and dy == 0:
        puzzle[empty_index[0]][empty_index[1]], puzzle[empty_index[0] - 1][empty_index[1]] = puzzle[empty_index[0] - 1][
            empty_index[1]], puzzle[empty_index[0]][empty_index[1]]
    else:
        raise ValueError("Invalid move!")

    return puzzle


def draw_button(screen, button_text, x, y, width, height, idle_color, hover_color, clicked_color, number_images,
                action=None):
    mouse_pos = pygame.mouse.get_pos()
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        current_color = hover_color
    else:
        current_color = idle_color
    if current_color == hover_color and pygame.mouse.get_pressed()[0]:
        if action is not None:
            action(screen, number_images)
    pygame.draw.rect(screen, current_color, (x, y, width, height))
    font = pygame.font.Font(None, 20)
    text_surface = font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


def run_dfs_limite(screen, number_images):
    liste = [[1, 0, 2], [8, 4, 3], [7, 6, 5]]
    path, pas = recherche_dfs_limite(liste, goal, True, 3)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    solved = False
    if liste == goal:
        solved = True

    path_index = 1
    draw_tiles(screen, liste, number_images)
    while path_index < len(path) and solved == False:
        if path_index % 3 == 0:
            draw_tiles(screen, path[path_index], number_images)
            liste = path[path_index]
            path_index += 1
        liste = move_tile(liste, path[path_index])
        path_index += 1
        screen.fill(WHITE)
        draw_grid(screen)
        draw_tiles(screen, liste, number_images)
        font = pygame.font.Font(None, 24)
        text = font.render("Pas: " + str(pas), True, BLACK)
        screen.blit(text, (400, 50))
        pygame.display.flip()
        clock.tick(1)

    while solved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solved = False

        screen.fill(WHITE)
        draw_grid(screen)
        draw_tiles(screen, liste, number_images)


def run_dfs(screen, number_images):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    solved = False
    liste = [[1, 0, 2], [8, 4, 3], [7, 6, 5]]
    path, pas = recherche_dfs(liste, goal, True)
    path_index = 1
    if liste == goal:
        print("Reached the goal state!")
        solved = True

    while path_index <= pas and not solved:
        liste = move_tile(liste, path[path_index])
        path_index += 1
        screen.fill(WHITE)
        draw_grid(screen)
        draw_tiles(screen, liste, number_images)
        font = pygame.font.Font(None, 24)
        text = font.render("Pas: " + str(pas), True, BLACK)
        text = font.render("Pas: " + str(pas), True, BLACK)
        screen.blit(text, (400, 50))
        pygame.display.flip()
        clock.tick(1)

    while solved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solved = False

        screen.fill(WHITE)
        draw_grid(screen)
        draw_tiles(screen, liste, number_images)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    liste = liste = [[1, 0, 2], [8, 4, 3], [7, 6, 5]]
    # path , pas = run_dfs_limite()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8-Puzzle Solver")

    clock = pygame.time.Clock()
    number_images = load_number_images()
    solved = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_grid(screen)
        draw_tiles(screen, liste, number_images)

        dfs_button_x = 300
        dfs_button_y = screen.get_height() - button_height - button_margin
        draw_button(screen, "DFS", dfs_button_x, dfs_button_y, button_width, button_height,
                    (200, 200, 200), (230, 230, 230), (180, 180, 180), number_images, run_dfs)

        lds_button_x = dfs_button_x + button_width + button_margin
        lds_button_y = dfs_button_y
        draw_button(screen, "LDS (Limited)", lds_button_x, lds_button_y, button_width, button_height,
                    (200, 200, 200), (230, 230, 230), (180, 180, 180), number_images, run_dfs_limite)

        pygame.display.flip()
        clock.tick(1)

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


if __name__ == "__main__":
    main()
