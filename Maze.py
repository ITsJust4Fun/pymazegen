import pygame
import random


class Cell:
    def __init__(self):
        self.right = True
        self.bottom = True

    def set_right(self, value: bool):
        self.right = value

    def set_bottom(self, value: bool):
        self.bottom = value


class Maze:
    def __init__(self, screen, size: tuple[int, int]):
        self.screen = screen
        self.maze = []
        self.row_count, self.column_count = size

    def fill(self):
        for x in range(0, self.row_count):
            self.maze.append([])
            for y in range(0, self.column_count):
                self.maze[x].append(Cell())

    def generate(self):
        self.fill()

        for x in range(0, self.row_count):
            for y in range(0, self.column_count):
                if x != 0:
                    if random.uniform(0, 1) >= 0.5:
                        if y != self.column_count - 1:
                            self.maze[x][y].set_right(False)
                        else:
                            self.maze[x-1][y].set_bottom(False)
                    else:
                        self.maze[x-1][y].set_bottom(False)
                else:
                    if y != self.column_count - 1:
                        self.maze[x][y].set_right(False)



    def render(self, pos: tuple[int, int], block_size: int,
               color: tuple[int, int, int]):

        pos_x, pos_y = pos
        height = block_size * self.row_count
        width = block_size * self.column_count

        for x in range(pos_x, width + pos_x, block_size):
            for y in range(pos_y, height + pos_y, block_size):
                index_x = (x - pos_x) // block_size
                index_y = (y - pos_y) // block_size

                if self.maze[index_y][index_x].right:
                    pygame.draw.line(self.screen, color, (x + block_size, y), (x + block_size, y + block_size), 1)

                if self.maze[index_y][index_x].bottom:
                    pygame.draw.line(self.screen, color, (x, y + block_size), (x + block_size, y + block_size), 1)

                if y == pos_y:
                    pygame.draw.line(self.screen, color, (x, y), (x + block_size, y), 1)

                if x == pos_x:
                    pygame.draw.line(self.screen, color, (x, y), (x, y + block_size), 1)
