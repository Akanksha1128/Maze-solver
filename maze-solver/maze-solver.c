#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Node structure to represent positions
typedef struct {
    int x, y;
} Node;

// Stack structure for managing nodes
typedef struct {
    Node *nodes;
    int top;
    int max_size;
} Stack;

void push(Stack *stack, int x, int y) {
    stack->nodes[++stack->top].x = x;
    stack->nodes[stack->top].y = y;
}

Node pop(Stack *stack) {
    return stack->nodes[stack->top--];
}

bool isEmpty(Stack *stack) {
    return stack->top == -1;
}

// Function to check if a move is valid
bool isValid(int **maze, int rows, int cols, int x, int y, bool **visited) {
    return (x >= 0 && x < rows && y >= 0 && y < cols && maze[x][y] == 1 && !visited[x][y]);
}

// Function to print the path
void printPath(Node path[], int length) {
    for (int i = 0; i < length; i++) {
        printf("(%d, %d) ", path[i].x, path[i].y);
    }
    printf("\n");
}

// Function to visually represent the maze with the path
void printMazeWithPath(int **maze, int rows, int cols, Node path[], int length) {
    char **visualMaze = (char **)malloc(rows * sizeof(char *));
    for (int i = 0; i < rows; i++) {
        visualMaze[i] = (char *)malloc(cols * sizeof(char));
    }

    // Copy maze data to visualMaze, marking path cells
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            visualMaze[i][j] = maze[i][j] == 1 ? '.' : '#';
        }
    }

    // Mark the path in visualMaze
    for (int i = 0; i < length; i++) {
        int x = path[i].x;
        int y = path[i].y;
        visualMaze[x][y] = 'P'; // 'P' for path
    }

    // Print the visual representation of the maze
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%c ", visualMaze[i][j]);
        }
        printf("\n");
    }
    printf("\n");

    // Free allocated memory
    for (int i = 0; i < rows; i++) {
        free(visualMaze[i]);
    }
    free(visualMaze);
}

void solveMaze(int **maze, int rows, int cols) {
    // Check if start or goal is blocked
    if (maze[0][0] == 0 || maze[rows - 1][cols - 1] == 0) {
        printf("No solution found\n");
        return;
    }

    bool **visited = (bool **)malloc(rows * sizeof(bool *));
    for (int i = 0; i < rows; i++) {
        visited[i] = (bool *)calloc(cols, sizeof(bool));
    }

    Node *path = (Node *)malloc(rows * cols * sizeof(Node));
    Stack cpstack = { .nodes = (Node *)malloc(rows * cols * sizeof(Node)), .top = -1, .max_size = rows * cols };
    int pathIndex = 0;

    // Start from (0, 0)
    push(&cpstack, 0, 0);
    visited[0][0] = true;
    path[pathIndex++] = (Node){0, 0};

    while (!isEmpty(&cpstack)) {
        Node current = cpstack.nodes[cpstack.top];
        int x = current.x;
        int y = current.y;

        // If goal is reached, print the path and maze
        if (x == rows - 1 && y == cols - 1) {
            printPath(path, pathIndex);
            printMazeWithPath(maze, rows, cols, path, pathIndex);
            
            // Free allocated memory and exit
            free(cpstack.nodes);
            free(path);
            for (int i = 0; i < rows; i++) {
                free(visited[i]);
            }
            free(visited);
            return;
        }

        // Explore neighbors in right, down, left, up order
        int newPositions[4][2] = {
            {x, y + 1},  // Right
            {x + 1, y},  // Down
            {x, y - 1},  // Left
            {x - 1, y}   // Up
        };

        bool foundValidMove = false;

        for (int i = 0; i < 4; i++) {
            int newX = newPositions[i][0];
            int newY = newPositions[i][1];

            if (isValid(maze, rows, cols, newX, newY, visited)) {
                push(&cpstack, newX, newY);
                visited[newX][newY] = true;
                path[pathIndex++] = (Node){newX, newY};
                foundValidMove = true;
                break; // Move to the next iteration of the while loop
            }
        }

        if (!foundValidMove) {
            // Backtrack
            pop(&cpstack);  // Remove the last position from the stack
            pathIndex--;    // Remove the last position from the path
        }
    }

    printf("No solution found\n");

    // Free allocated memory
    free(cpstack.nodes);
    free(path);
    for (int i = 0; i < rows; i++) {
        free(visited[i]);
    }
    free(visited);
}

int main() {
    int rows, cols;
    printf("Enter the number of rows and columns for the maze: ");
    scanf("%d %d", &rows, &cols);

    // Dynamically allocate the maze
    int **maze = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        maze[i] = (int *)malloc(cols * sizeof(int));
    }

    printf("Enter the maze (0 for wall, 1 for path):\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &maze[i][j]);
        }
    }

    solveMaze(maze, rows, cols);

    // Free allocated memory for the maze
    for (int i = 0; i < rows; i++) {
        free(maze[i]);
    }
    free(maze);

    return 0;
}