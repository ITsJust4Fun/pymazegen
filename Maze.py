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


class Value:
    def __init__(self):
        self.x1 = 0  # horizontal interval
        self.x2 = 0

        self.y1 = 0  # vertical interval
        self.y2 = 0

        self.is_horizontal = True
        self.wall_position = 0
        self.door_position = 0


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = None



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

    def import_file(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()

            for line in lines:
                self.maze.append([])
                for letter in line:
                    if letter.isdigit():
                        cell = Cell()
                        digit = int(letter)

                        if digit == 0:
                            cell.bottom = False
                            cell.right = False
                        elif digit == 1:
                            cell.bottom = False
                        elif digit == 2:
                            cell.right = False

                        self.maze[-1].append(cell)

            self.row_count = len(self.maze)
            self.column_count = len(self.maze[0])

    def generate_binary(self, node: Node, x1, x2, y1, y2):
        if x2 - x1 == 0 and y2 - y1 == 0:
            return

        node.value.is_horizontal = random.uniform(0, 1) >= 0.5

        if node.value.is_horizontal:
            node.value.wall_position = int(random.uniform(y1, y2))
            node.value.door_position = int(random.uniform(x1, x2))

            self.generate_binary(node.left, x1, x2, y1, node.value.wall_position)
            self.generate_binary(node.right, x1, x2, node.value.wall_position + 1, y2)
        else:
            node.value.wall_position = int(random.uniform(x1, x2))
            node.value.door_position = int(random.uniform(y1, y2))

            self.generate_binary(node.left, x1, node.value.wall_position, y1, y2)
            self.generate_binary(node.right, node.value.wall_position + 1, x2, y1, y2)

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
