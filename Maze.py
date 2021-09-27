import pygame
import random


class Cell:
    def __init__(self):
        self.right = True
        self.bottom = True
        self.is_path = False
        self.is_visited = False

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
        self.last = False


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = Value()


class Path:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.next = None


class NodePath:
    def __init__(self):
        self.cell = Cell()
        self.parent = None
        self.right = None
        self.left = None


class Maze:
    def __init__(self, screen, size: tuple[int, int]):
        self.screen = screen
        self.maze = []
        self.final_node = None
        self.row_count, self.column_count = size

    def fill(self):
        for x in range(0, self.row_count):
            self.maze.append([])
            for y in range(0, self.column_count):
                self.maze[x].append(Cell())

    def fill_empty(self):
        for x in range(0, self.row_count):
            self.maze.append([])
            for y in range(0, self.column_count):
                cell = Cell()
                if y != self.column_count - 1:
                    cell.right = False
                if x != self.row_count - 1:
                    cell.bottom = False

                self.maze[x].append(cell)

    def tree_to_table(self, node):
        if node.value.last:
            return

        if node.value.is_horizontal:
            for i in range(node.value.x1, node.value.x2 + 1):
                is_wall = i != node.value.door_position
                self.maze[node.value.wall_position][i].bottom = is_wall
        else:
            for i in range(node.value.y1, node.value.y2 + 1):
                is_wall = i != node.value.door_position
                self.maze[i][node.value.wall_position].right = is_wall

        self.tree_to_table(node.left)
        self.tree_to_table(node.right)

    def generate_node(self, x1, x2, y1, y2):
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0 or x1 > x2 or y1 > y2:
            return None

        node = Node()
        node.value.x1 = x1
        node.value.x2 = x2
        node.value.y1 = y1
        node.value.y2 = y2

        if x2 == x1 and y2 == y1:
            node.value.last = True
        else:
            node.value.last = False
            node.value.is_horizontal = not not random.randrange(0, 2)

            if node.value.is_horizontal and y2 == y1:
                node.value.is_horizontal = False
            elif not node.value.is_horizontal and x2 == x1:
                node.value.is_horizontal = True

            if node.value.is_horizontal:
                node.value.wall_position = (y2 + y1) // 2
                node.value.door_position = random.randrange(x1, x2 + 1)

                node.left = self.generate_node(x1, x2, y1, node.value.wall_position)
                node.right = self.generate_node(x1, x2, node.value.wall_position + 1, y2)
            else:
                node.value.wall_position = (x2 + x1) // 2
                node.value.door_position = random.randrange(y1, y2 + 1)

                node.left = self.generate_node(x1, node.value.wall_position, y1, y2)
                node.right = self.generate_node(node.value.wall_position + 1, x2, y1, y2)

        return node

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

        self.get_full_tree_path(0, 0, self.row_count - 1, self.column_count - 1)

    def generate_tree(self):
        n, m = self.row_count, self.column_count

        node = self.generate_node(0, m - 1, 0, n - 1)
        self.fill_empty()
        self.tree_to_table(node)
        self.get_full_tree_path(0, 0, self.row_count - 1, self.column_count - 1)
        # path = self.get_full_path(node, 0, 0, m - 1, n - 1)
        # self.add_path_to_maze(path)

    def get_full_tree_path(self, x1, y1, x2, y2):
        start_cell = self.maze[x1][y1]
        end_cell = self.maze[x2][y2]

        self.get_node_path(start_cell, end_cell, x1, y1)

        while self.final_node:
            self.final_node.cell.is_path = True
            self.final_node = self.final_node.parent

    def get_node_path(self, start_cell, end_cell, x, y):
        node = NodePath()
        node.cell = start_cell
        self.maze[x][y].is_visited = True

        if start_cell != end_cell:
            if not start_cell.right and not self.maze[x][y + 1].is_visited:
                node.left = self.get_node_path(self.maze[x][y + 1], end_cell, x, y + 1)
                node.left.parent = node
            if not start_cell.bottom and not self.maze[x + 1][y].is_visited:
                node.right = self.get_node_path(self.maze[x + 1][y], end_cell, x + 1, y)
                node.right.parent = node
            if (y - 1) >= 0 and not self.maze[x][y - 1].right and not self.maze[x][y - 1].is_visited:
                node.left = self.get_node_path(self.maze[x][y - 1], end_cell, x, y - 1)
                node.left.parent = node
            if (x - 1) >= 0 and not self.maze[x - 1][y].bottom and not self.maze[x - 1][y].is_visited:
                node.left = self.get_node_path(self.maze[x - 1][y], end_cell, x - 1, y)
                node.left.parent = node
        else:
            self.final_node = node

        return node

    def get_path(self, node, x1, y1, pp, pd):
        path = Path()

        if node.value.last:
            path.x1 = node.value.x1
            path.y1 = node.value.y1
        elif node.value.is_horizontal:
            path.x1 = node.value.door_position
            path.y1 = node.value.wall_position

            if node.right and y1 >= node.right.value.y1 and y1 <= node.right.value.y2 and x1 >= node.right.value.x1 and x1 <= node.right.value.x2:
                if (pd == 1 and pp >= node.right.value.y1 and pp <= node.right.value.y2) or (pd == 0 and pp >= node.right.value.x1 and pp <= node.right.value.x2):
                    path = self.get_path(node.right, x1, y1, node.value.door_position, node.value.is_horizontal)
                else:
                    path.next = self.get_path(node.right, x1, y1, node.value.door_position, node.value.is_horizontal)
            elif node.left and y1 >= node.left.value.y1 and y1 <= node.left.value.y2 and x1 >= node.left.value.x1 and x1 <= node.left.value.x2:
                 if (pd == 1 and pp >= node.left.value.y1 and pp <= node.left.value.y2) or (pd == 0 and pp >= node.left.value.x1 and pp <= node.left.value.x2):
                     path = self.get_path(node.left, x1, y1, node.value.door_position, node.value.is_horizontal)
                 else:
                    path.next = self.get_path(node.left, x1, y1, node.value.door_position, node.value.is_horizontal)
        else:
            path.y1 = node.value.door_position
            path.x1 = node.value.wall_position

            if node.right and y1 >= node.right.value.y1 and y1 <= node.right.value.y2 and x1 >= node.right.value.x1 and x1 <= node.right.value.x2:
                if(pd == 1 and pp >= node.right.value.y1 and pp <= node.right.value.y2) or (pd == 0 and pp >= node.right.value.x1 and pp <= node.right.value.x2):
                    path = self.get_path(node.right, x1, y1, node.value.door_position, node.value.is_horizontal)
                else:
                    path.next = self.get_path(node.right, x1, y1, node.value.door_position, node.value.is_horizontal)
            elif node.left and y1 >= node.left.value.y1 and y1 <= node.left.value.y2 and x1 >= node.left.value.x1 and x1 <= node.left.value.x2:
                if (pd == 1 and pp >= node.left.value.y1 and pp <= node.left.value.y2) or (pd == 0 and pp >= node.left.value.x1 and pp <= node.left.value.x2):
                    path = self.get_path(node.left, x1, y1, node.value.door_position, node.value.is_horizontal)
                else:
                    path.next = self.get_path(node.left, x1, y1, node.value.door_position, node.value.is_horizontal)

        return path

    def get_full_path(self, node, x1, y1, x2, y2):
        start = self.get_path(node, x1, y1, -1, -1)
        end = self.get_path(node, x2, y2, -1, -1)
        mid = start
        while start.next and end.next and start.next.x1 == end.next.x1 and start.next.y == end.next.y:
            start = start.next
            end = end.next
        while mid.next:
            mid = mid.next
        mid.next = end

        return start

    def add_path_to_maze(self, path):
        while path.next:
            self.maze[path.y1][path.x1].is_path = True
            path = path.next

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
                    pygame.draw.line(self.screen, color, (x + block_size, y), (x + block_size, y + block_size), 2)

                if self.maze[index_y][index_x].bottom:
                    pygame.draw.line(self.screen, color, (x, y + block_size), (x + block_size, y + block_size), 2)

                if self.maze[index_y][index_x].is_path:
                    rect = pygame.Rect(x + 3, y + 3, block_size - 4, block_size - 4)
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)

                if y == pos_y:
                    pygame.draw.line(self.screen, color, (x, y), (x + block_size, y), 2)

                if x == pos_x:
                    pygame.draw.line(self.screen, color, (x, y), (x, y + block_size), 2)
