# 🧩 Maze Solver in C

[![C](https://img.shields.io/badge/Language-C-blue.svg)](https://en.wikipedia.org/wiki/C_(programming_language))

This project is a **stack-based maze solver** written in **C**, which finds a valid path from the start (top-left corner) to the end (bottom-right corner) of a maze. It uses a custom stack implementation and **depth-first search (DFS)** to explore all possible paths.

---

## 🔍 Overview

- Accepts user input for the maze dimensions and structure.
- Navigates from `(0, 0)` to `(rows-1, cols-1)` if a path exists.
- Uses a stack to simulate recursive DFS traversal.
- Backtracks automatically when a dead end is reached.
- Outputs the **solution path** and a **visual representation** of the maze with the path marked.

---

## 📁 File Structure

- `maze-solver.c` — Main source code file containing:
  - Maze input & validation
  - DFS logic using a stack
  - Visual maze printer with marked path
  - Memory cleanup

---

## ⚙️ How to Compile and Run

### 🧰 Compile:
```bash
gcc maze-solver.c -o maze-solver
