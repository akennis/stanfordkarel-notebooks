# Changelog

## 0.2.7 (2026-04-06)

Initial release of `stanfordkarel-notebooks`.

### Added

- Jupyter/IPython notebook support via `KarelImageRenderer`: Karel programs render as
  animated GIFs displayed inline in notebooks, with no desktop display required.
- `run_karel_program()` accepts `main_func=` to run a Karel program directly from a
  function reference, enabling notebook-style usage without a `.py` student file.
- `KarelWorld` can be constructed from an inline `world_text=` string or a remote
  `world_url=` (fetched via HTTP), in addition to local `.w` files.
- `StudentCode` accepts `main_func=` to wrap an in-memory function as student code.

### Changed (from TylerYep/stanfordkarel)

- Removed the desktop tkinter GUI (`KarelApplication`, `KarelCanvas`), ASCII renderer,
  and world editor. These are not available in headless/cloud Jupyter environments.
- `run_karel_program()` no longer opens a desktop window. The `main_func=` parameter
  is now required.
- Package renamed to `stanfordkarel-notebooks` to distinguish from the upstream library.
