import pygame
from DebugInfo import DebugInfo
from Maze import Maze


maze_size = (50, 50)
maze_block_size = 10
speed = 1
WINDOW_SIZE = (1800, 1000)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Maze')
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    clock = pygame.time.Clock()

    debug_info = DebugInfo(screen, clock)
    debug_options = {'fps': True, 'frametime': True, 'frametime_graph': True, 'frametime_peek': True}

    maze = Maze(screen, maze_size)
    #maze.generate()
    maze.import_file('5x5.txt')
    maze_size = maze.column_count, maze.row_count

    maze_pos = ((WINDOW_SIZE[0] // 2) - (maze_size[0] * maze_block_size // 2),
                (WINDOW_SIZE[1] // 2) - (maze_size[1] * maze_block_size // 2))

    n, m = 5, 5
    k = 0

    node = maze.generate_binary(0, m - 1, 0, n - 1)
    table = []

    for i in range(0, 2 * n + 1):
        table.append([])
        table[i] = [' '] * (2 * m + 1)
        for j in range(0, 2 * m + 1):
            if i == 0 or j == 0 or i == 2 * n or j == 2 * m:
                table[i][j] = '#'

    maze.generate_table(node, table, n, m)

    for i in range(0, len(table)):
        for j in table[i]:
            print(j, end='')
        print('\n', end='')


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and maze_block_size - 1:
                    maze_block_size -= 1 * speed
                if event.button == 5:
                    maze_block_size += 1 * speed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_PLUS:
                    maze_block_size += 1
                if event.key == pygame.K_KP_MINUS:
                    maze_block_size -= 1

        if maze_block_size >= 10:
            speed = maze_block_size // 10

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            maze_pos = maze_pos[0] - 1 * speed * 10, maze_pos[1]

        if keys[pygame.K_RIGHT]:
            maze_pos = maze_pos[0] + 1 * speed * 10, maze_pos[1]

        if keys[pygame.K_UP]:
            maze_pos = maze_pos[0], maze_pos[1] - 1 * speed * 10

        if keys[pygame.K_DOWN]:
            maze_pos = maze_pos[0], maze_pos[1] + 1 * speed * 10
        #
        # if keys[pygame.K_KP_PLUS]:
        #     maze_block_size += 1 * speed
        #
        # if keys[pygame.K_KP_MINUS]:
        #     maze_block_size -= 1 * speed

        clock.tick(60)

        screen.fill(WHITE)
        maze.render(maze_pos, maze_block_size, BLACK)
        debug_info.render(debug_options)

        pygame.display.flip()

    pygame.quit()
