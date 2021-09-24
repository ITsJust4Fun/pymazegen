#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <iostream>

class Cell
{
public:
	bool visited = false;
	bool bottom_wall = true;
	bool right_wall = true;
};

class Maze
{
private:
	std::string directions[4] = { "UP", "DOWN", "LEFT", "RIGHT" };
	std::vector<std::vector<Cell>> MazeGrid;
public:
	void createGrid(int rows, int columns);
	void createMaze(int, int);
};

void Maze::createGrid(int rows, int columns)
{
	for (int y = 0; y < rows; y++)
	{
		MazeGrid.push_back(std::vector<Cell>());
		for (int x = 0; x < columns; x++)
		{
			Cell cell;
			MazeGrid[y].push_back(cell);
		}
	}
}

void Maze::createMaze(int rows, int columns)
{
	createGrid(rows, columns);

	int unvisited_cells = rows * columns;
	int ix = rand() % columns;
	int iy = rand() % rows;

	MazeGrid[iy][ix].visited = true;
	unvisited_cells--;

	while (unvisited_cells != 0)
	{
		std::string dir = directions[rand() % 4];
		std::cout << iy << " " << ix << " " << dir << " " << unvisited_cells << std::endl;

		if (dir == "UP")
		{
			if (iy - 1 >= 0)
			{
				if (MazeGrid[iy - 1][ix].visited == false)
				{
					MazeGrid[iy - 1][ix].bottom_wall = false;
					MazeGrid[iy - 1][ix].visited = true;
					unvisited_cells--;
				}

				iy--;
			}
		}
		else if (dir == "DOWN")
		{
			if (iy + 1 <= rows-1)
			{
				if (MazeGrid[iy + 1][ix].visited == false)
				{
					MazeGrid[iy][ix].bottom_wall = false;
					MazeGrid[iy + 1][ix].visited = true;
					unvisited_cells--;
				}

				iy++;
			}
		}
		else if (dir == "RIGHT")
		{
			if (ix + 1 <= columns - 1)
			{
				if (MazeGrid[iy][ix + 1].visited == false)
				{
					MazeGrid[iy][ix].right_wall = false;
					MazeGrid[iy][ix + 1].visited = true;
					unvisited_cells--;
				}

				ix++;
			}
		}
		else if (dir == "LEFT")
		{
			if (ix - 1 >= 0)
			{
				if (MazeGrid[iy][ix - 1].visited == false)
				{
					MazeGrid[iy][ix - 1].right_wall = false;
					MazeGrid[iy][ix - 1].visited = true;
					unvisited_cells--;
				}

				ix--;
			}
		}
	}
	std::ofstream fout;
	fout.open("file.txt");
	for (int y = 0; y < rows; y++)
	{
		for (int x = 0; x < columns; x++)
		{
			if (MazeGrid[y][x].bottom_wall == false && MazeGrid[y][x].right_wall == false)
			{
				fout << "0";
			}
			else if (MazeGrid[y][x].bottom_wall == false && MazeGrid[y][x].right_wall == true)
			{
				fout << "1";
			}
			else if (MazeGrid[y][x].bottom_wall == true && MazeGrid[y][x].right_wall == false)
			{
				fout << "2";
			}
			else
			{
				fout << "3";
			}
		}
		fout << "\n";
	}
}

int main()
{
	Maze maze;
	maze.createMaze(50, 50);
	return 0;
}
