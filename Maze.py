import pygame
import random
import math


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
        self.last = 0


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = Value()


class Path:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.next = None


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

    def generate_table(self, node, table, n, m):
        if not node:
            return

        for i in range(0, 2 * n + 1):
            table.append([])
            table[i] = [' '] * (2 * m + 1)
            for j in range(0, 2 * m + 1):
                if i == 0 or j == 0 or i == 2 * n or j == 2 * m:
                    table[i][j] = '#'

        if node.value.is_horizontal:
            for i in range(2 * node.value.x1 + 1, 2 * (node.value.x2 + 1)):
                table[2 * (node.value.wall_position + 1)][i] = '#'
            table[2 * (node.value.wall_position + 1)][2 * node.value.door_position + 1] = ' '
        else:
            for i in range(2 * node.value.y1 + 1, 2 * (node.value.y2 + 1)):
                table[i][2 * (node.value.wall_position + 1)] = '#'
            table[2 * node.value.door_position + 1][2 * (node.value.wall_position + 1)] = ' '

        if node.value.last:
            self.generate_table(node.left, table, n, m)
            self.generate_table(node.right, table, n, m)

    def generate_binary(self, x1, x2, y1, y2):
        if x1 <= 0 or x2 <= 0 or y1 <= 0 or y2 <= 0 or x1 > x2 or y1 > y2:
            return None

        node = Node()
        node.value.x1 = x1
        node.value.x2 = x2
        node.value.y1 = y1
        node.value.y2 = y2

        if x2 - x1 == 0 and y2 - y1 == 0:
            node.value.last = 1
        else:
            node.value.last = 0
            node.value.is_horizontal = not not random.randrange(0, 2)

            if node.value.is_horizontal and y2 - y1 == 0:
                node.value.is_horizontal = False
            else:
                node.value.is_horizontal = True

            if node.value.is_horizontal:
                node.value.wall_position = math.floor((y2 - y1) / 2)
                node.value.door_position = random.randrange(x1, x2 + 1) if x2 != 0 else 0

                node.left = self.generate_binary(x1, x2, y1, node.value.wall_position)
                node.right = self.generate_binary(x1, x2, node.value.wall_position + 1, y2)
            else:
                node.value.wall_position = math.floor((x2 - x1) / 2)
                node.value.door_position = random.randrange(y1, y2 + 1) if y2 != 0 else 0

                node.left = self.generate_binary(x1, node.value.wall_position, y1, y2)
                node.right = self.generate_binary(node.value.wall_position + 1, x2, y1, y2)

        return node

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
