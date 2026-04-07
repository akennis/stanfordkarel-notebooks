"""Tests for notebook-specific features added in stanfordkarel-notebooks."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from stanfordkarel.karel_image_renderer import KarelImageRenderer
from stanfordkarel.karel_program import KarelProgram
from stanfordkarel.stanfordkarel import run_karel_program
from stanfordkarel.student_code import StudentCode

SIMPLE_WORLD = "Dimension: (5, 5)\nKarel: (1, 1); east"


def main() -> None:
    """No-op Karel main function used as a test fixture."""


class TestMainFunc:
    @staticmethod
    def test_student_code_accepts_callable() -> None:
        """StudentCode stores the module of the provided callable."""
        code = StudentCode(main_func=main)
        assert code.mod is not None

    @staticmethod
    def test_student_code_raises_without_args() -> None:
        """StudentCode raises FileNotFoundError when no code_file or main_func given."""
        with pytest.raises(FileNotFoundError):
            StudentCode()

    @staticmethod
    def test_main_func_is_called() -> None:
        """StudentCode(main_func=main).main() delegates to the module's main()."""
        code = StudentCode(main_func=main)
        code.main()  # no-op; succeeds because this module exports `main`


class TestWorldText:
    @staticmethod
    def test_karel_program_loads_from_text() -> None:
        """KarelProgram correctly parses world_text=."""
        karel = KarelProgram(world_text=SIMPLE_WORLD)
        assert karel.avenue == 1
        assert karel.street == 1

    @staticmethod
    def test_karel_program_raises_without_world_source() -> None:
        """KarelProgram raises ValueError when neither world_url nor world_text given."""  # noqa: E501
        with pytest.raises(ValueError, match="world_url or world_text"):
            KarelProgram()


class TestWorldUrl:
    @staticmethod
    def test_karel_program_loads_from_url() -> None:
        """KarelProgram fetches and parses world text from a URL."""
        mock_response = MagicMock()
        mock_response.read.return_value = SIMPLE_WORLD.encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            karel = KarelProgram(world_url="https://example.com/world.w")

        assert karel.avenue == 1
        assert karel.street == 1


class TestIPythonRenderer:
    @staticmethod
    def test_raises_clear_error_without_ipython() -> None:
        """A missing IPython install raises ImportError with an install hint."""
        karel = KarelProgram(world_text=SIMPLE_WORLD)
        renderer = KarelImageRenderer(karel.world, karel)
        student_code = StudentCode(main_func=main)

        with (
            patch.dict(sys.modules, {"IPython.display": None}),
            pytest.raises(ImportError, match="stanfordkarel-notebooks\\[notebook\\]"),
        ):
            renderer.run_and_render_to_ipython(student_code)

    @staticmethod
    def test_renders_gif_when_ipython_available() -> None:
        """IPython display is called with GIF data when IPython is installed."""
        pytest.importorskip("IPython")

        karel = KarelProgram(world_text=SIMPLE_WORLD)
        renderer = KarelImageRenderer(karel.world, karel)
        student_code = StudentCode(main_func=main)

        with (
            patch("IPython.display.display") as mock_display,
            patch("IPython.display.Image", return_value=MagicMock()),
        ):
            renderer.run_and_render_to_ipython(student_code)

        mock_display.assert_called_once()


class TestSpeedValidation:
    @staticmethod
    def test_speed_above_100_raises() -> None:
        """speed > 100 raises ValueError before any rendering occurs."""
        with pytest.raises(ValueError, match="speed"):
            run_karel_program(world_text=SIMPLE_WORLD, main_func=main, speed=101)

    @staticmethod
    def test_speed_below_0_raises() -> None:
        """speed < 0 raises ValueError before any rendering occurs."""
        with pytest.raises(ValueError, match="speed"):
            run_karel_program(world_text=SIMPLE_WORLD, main_func=main, speed=-1)

    @staticmethod
    def test_speed_at_boundaries_accepted() -> None:
        """speed=0 and speed=100 are valid values and do not raise."""
        with patch(
            "stanfordkarel.karel_image_renderer.KarelImageRenderer.run_and_render_to_ipython"
        ):
            run_karel_program(world_text=SIMPLE_WORLD, main_func=main, speed=0)
            run_karel_program(world_text=SIMPLE_WORLD, main_func=main, speed=100)
