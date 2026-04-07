# stanfordkarel-notebooks

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![GitHub license](https://img.shields.io/github/license/akennis/stanfordkarel-notebooks)](https://github.com/akennis/stanfordkarel-notebooks/blob/main/LICENSE)

A fork of [TylerYep/stanfordkarel](https://github.com/TylerYep/stanfordkarel) — the Python implementation of Karel used in Stanford's CS 106A — extended with **Jupyter notebook support**. Karel programs run directly inside notebooks as animated GIFs, with no desktop window required.

---

## Installation

```bash
pip install git+https://github.com/akennis/stanfordkarel-notebooks.git
```

---

## For Educators

### Why Karel in a Notebook?

Jupyter notebooks let you combine executable code, explanatory text, images, and output in a single document. For a Karel-based introductory course, this means you can build an entire curriculum — textbook chapters, lab exercises, homework assignments, and automated tests — as notebooks that students open and run directly, without any IDE setup.

**Notebook-based textbooks and readings.** A chapter on loops or conditionals can place a Karel world, the problem description, and a code cell for the student's solution all on the same page. Students read the concept, see it illustrated with Karel, and write code immediately — in the same document.

**Labs and in-class exercises.** Each lab is a notebook. You distribute it, students fill in the code cells, run them, and see Karel animate. The animation appears inline so the feedback loop is immediate: write code → run cell → watch Karel move → adjust. No file management, no terminal.

**Homework assignments.** Students submit their notebook. You can include assertion cells at the bottom that compare the resulting Karel world to the expected end state, giving students instant pass/fail feedback before they submit.

**Testing and autograding.** The notebook renderer runs Karel headlessly and captures each step as a frame, so notebooks can run in CI or an autograder without a display. You can call `run_karel_program` with `main_func=` pointing to the student's function, check the resulting world programmatically, and report results — all within the notebook.

### Setting Up a Course Notebook

A typical assignment notebook cell looks like this:

```python
from stanfordkarel import *

def main():
    # Students write their solution here
    move()
    turn_left()
    move()

run_karel_program(world_text="Dimension: (5, 5)\nKarel: (1, 1); east", main_func=main)
```

When the student runs the cell, Karel's animated execution appears inline.

To load a world from a URL instead, pass a string URL:

```python
run_karel_program(world_url="https://raw.githubusercontent.com/.../my_world.w", main_func=main)
```

To test programmatically in the same notebook:

```python
from stanfordkarel.karel_program import KarelProgram
from stanfordkarel.karel_executor import inject_karel_api
from stanfordkarel.student_code import StudentCode

karel = KarelProgram(world_text="Dimension: (5, 5)\nKarel: (1, 1); east")
inject_karel_api(StudentCode(main_func=main), karel)
# run karel.main() and compare to expected world state
```

---

## For Students

### What is a Jupyter Notebook?

A Jupyter notebook is a document that mixes text, images, and runnable code cells. When your instructor gives you a notebook file (ending in `.ipynb`), you open it in a browser and work through it top to bottom. Each code cell has a **Run** button (or press **Shift+Enter**). You edit the code in the cell and run it to see what happens — the output appears directly below the cell.

### How You Will Use Karel

Karel is a simple robot that lives on a grid. It can move forward, turn left, pick up beepers, and put them down. Your job is to write Python instructions that tell Karel how to solve a puzzle.

In this course, each assignment is a notebook. You will:

1. **Read the problem** described in the notebook above the code cell.
2. **Write your solution** in the code cell by defining a `main()` function.
3. **Run the cell** (Shift+Enter). An animation will appear showing Karel executing your code step by step.
4. **Fix and re-run** until Karel solves the puzzle correctly.

A typical solution looks like this:

```python
from stanfordkarel import *

def main():
    move()
    turn_left()
    move()

run_karel_program(world_text="Dimension: (5, 5)\nKarel: (1, 1); east", main_func=main)
```

You do not need to install anything beyond what your instructor provides. Just open the notebook and start writing.

---

## Available Commands

| Karel Commands       |                        |                          |
| -------------------- | ---------------------- | ------------------------ |
| `move()`             | `right_is_clear()`     | `facing_east()`          |
| `turn_left()`        | `right_is_blocked()`   | `not_facing_east()`      |
| `put_beeper()`       | `beepers_present()`    | `facing_west()`          |
| `pick_beeper()`      | `no_beepers_present()` | `not_facing_west()`      |
| `front_is_clear()`   | `beepers_in_bag()`     | `facing_south()`         |
| `front_is_blocked()` | `no_beepers_in_bag()`  | `not_facing_south()`     |
| `left_is_clear()`    | `facing_north()`       | `paint_corner(color)`    |
| `left_is_blocked()`  | `not_facing_north()`   | `corner_color_is(color)` |

## Available Colors

Red, Black, Cyan, Dark Gray, Gray, Green, Light Gray, Magenta, Orange, Pink, White, Blue, Yellow

---

## `run_karel_program` Reference

```python
run_karel_program(
    world_url=None,       # URL string pointing to a .w world file
    world_text="",        # world definition as an inline string
    main_func=main,       # required: the function containing student code
    cell_size=50,         # pixel size of each grid cell in the animation
    speed=None,           # animation speed 0–100 (default: 50)
)
```

Exactly one of `world_url` or `world_text` must be provided. `main_func` is always required.

---

## World File Format

World files (`.w`) are plain text, one directive per line:

```
Dimension: (5, 5)
Karel: (1, 1); east
BeeperBag: INFINITY
Wall: (2, 1); north
Beeper: (3, 3) 2
Color: (4, 4); Red
Speed: 0.5
```

Key directives:

| Directive | Parameters |
| --- | --- |
| `Dimension` | `(avenues, streets)` |
| `Karel` | `(avenue, street); direction` |
| `Wall` | `(avenue, street); direction` |
| `Beeper` | `(avenue, street) count` |
| `BeeperBag` | `num_beepers` or `INFINITY` |
| `Color` | `(avenue, street); color` |
| `Speed` | delay as a float (0.0–1.0) |

---

## Folder Structure

For file-based worlds, place `.w` files in a `worlds/` folder next to the notebook. End-state worlds used for grading are named `<world>_end.w`.

```
assignment1/
  worlds/
    collect_newspaper_karel.w
    collect_newspaper_karel_end.w
  collect_newspaper_karel.ipynb
```

---

## Original Library

This fork is based on [TylerYep/stanfordkarel](https://github.com/TylerYep/stanfordkarel). This fork removes the desktop tkinter GUI, ASCII renderer, and world editor from the original library in order to support environments (such as cloud-hosted Jupyter) where a display is not available. The core Karel logic, world file format, style checker, and "did you mean?" suggestions are preserved.

---

## Contributing

- Install pre-commit hooks: `pip install pre-commit && pre-commit install`
- Run tests: `uv run pytest`
- Run type checking: `uv run mypy stanfordkarel/`
- Lint and format: `pre-commit run --all-files`

### Clean Rebuild

To remove all build artifacts and caches for a fresh rebuild:

```bash
uv run poe clean   # removes .venv, dist, build, caches, __pycache__, etc.
uv sync            # reinstalls dependencies
pre-commit install # reinstalls git hooks
```
