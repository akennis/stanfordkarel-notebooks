# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/functionality_test.py

# Run a single test by name
uv run pytest tests/functionality_test.py::test_name

# Type checking
uv run mypy stanfordkarel/

# Lint and format (via pre-commit)
pre-commit run --all-files

# Run ruff directly
uv run ruff check stanfordkarel/
uv run ruff format stanfordkarel/
```

**Note:** On this machine, bash output must be redirected to a file in the project directory and then read, e.g. `command > output.txt 2>&1`.

## Architecture

This is the official Stanford Karel library (CS 106A). Students write Karel programs using `from stanfordkarel import *`, then call `run_karel_program()` to run them.

### Execution flow

1. `stanfordkarel/stanfordkarel.py` — Public API stubs (IDE-visible) + `run_karel_program()` entry point. Instantiates `KarelProgram` and dispatches to a renderer.
2. `stanfordkarel/student_code.py` — `StudentCode`: loads the student's `.py` file as a module via `importlib`, extracts `main()`.
3. `stanfordkarel/karel_executor.py` — `inject_karel_api()` rebinds the stub functions in the student module to the live `KarelProgram` methods. `execute_student_program()` calls `student_code.main()` with optional per-action callbacks.
4. `stanfordkarel/karel_program.py` — `KarelProgram`: actual Karel logic (move, turn, beepers, walls). Also defines `KarelException`.
5. `stanfordkarel/karel_world.py` — `KarelWorld`: parses `.w` world files, stores walls/beepers/colors/Karel start position.

### Render modes (`render=` parameter)

- `"tk"` (default) — `KarelApplication` (tkinter GUI, `karel_application.py` + `karel_canvas.py`)
- `"gif"` — `KarelImageRenderer` renders to an animated GIF file using Pillow
- `"ipython"` — `KarelImageRenderer` renders to an animated GIF displayed inline in Jupyter notebooks

The `KarelBaseRenderer` abstract class (`karel_renderer.py`) contains shared drawing logic for both the GIF and tkinter renderers, using abstract `draw_line`, `draw_polygon`, `draw_text` methods.

### Key design pattern: API injection

Karel functions are defined as `raise NotImplementedError` stubs in `stanfordkarel.py` so IDEs can recognize them. At runtime, `inject_karel_api()` replaces them in the student's module namespace with bound methods from the live `KarelProgram` instance. This is why student code must use `from stanfordkarel import *`.

### Testing

- `tests/conftest.py` — `execute_karel_code()` helper loads a student file and compares the resulting world to a `*_end.w` file.
- Student solutions go in `solutions/` (not committed). Tests pass with a warning if `solutions/` doesn't exist.
- World files (`.w`) go in `worlds/`. End-state worlds are named `<problem>_end.w`.
- `problems/` contains reference implementations used to generate `*_end.w` files via `conftest.create_solution_worlds()`.

### World file format

Plain text, one directive per line: `KEYWORD: PARAMETERS`. Key directives:
- `Dimension: (avenues, streets)`
- `Karel: (avenue, street); direction`
- `Wall: (avenue, street); direction`
- `Beeper: (avenue, street) count`
- `BeeperBag: num_beepers` (or `INFINITY`)
- `Color: (avenue, street); color`
