import os
import subprocess
import sys
from pathlib import Path
import pytest


class TestExamples:
    """Test examples to ensure they run without errors"""

    @classmethod
    def setup_class(cls):
        """Setup for the test class"""
        cls.project_root = Path(__file__).parent.parent
        cls.examples_dir = cls.project_root / "examples"

    def _run_python_script(self, script_path: Path) -> tuple[int, str, str]:
        """
        Run a Python script and return the exit code, stdout, and stderr

        Args:
            script_path: Path to the Python script to run

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        try:
            # Change to the script's directory to handle relative imports/files correctly
            script_dir = script_path.parent
            result = subprocess.run(
                [sys.executable, script_path.name],
                cwd=script_dir,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout to prevent hanging
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Script execution timed out after 30 seconds"
        except Exception as e:
            return -1, "", f"Error running script: {str(e)}"

    def test_cell_quickstart(self):
        """Test cell quickstart example"""
        script_path = self.examples_dir / "cell" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Cell Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")  # Limit output for readability
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Cell quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_circle_quickstart(self):
        """Test circle quickstart example"""
        script_path = self.examples_dir / "circle" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Circle Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Circle quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_content_quickstart(self):
        """Test content quickstart example"""
        script_path = self.examples_dir / "content" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Content Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Content quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_ellipse_quickstart(self):
        """Test ellipse quickstart example"""
        script_path = self.examples_dir / "ellipse" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Ellipse Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Ellipse quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_line_quickstart(self):
        """Test line quickstart example"""
        script_path = self.examples_dir / "line" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Line Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Line quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_matrix_quickstart(self):
        """Test matrix quickstart example"""
        script_path = self.examples_dir / "matrix" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Matrix Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Matrix quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_matrix_border_as_number_demo(self):
        """Test matrix border as number demo example"""
        script_path = self.examples_dir / "matrix" / "border_as_number_demo.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Matrix Border Demo Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Matrix border demo failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_polyline_quickstart(self):
        """Test polyline quickstart example"""
        script_path = self.examples_dir / "polyline" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Polyline Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Polyline quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )

    def test_rectangle_quickstart(self):
        """Test rectangle quickstart example"""
        script_path = self.examples_dir / "rectangle" / "quickstart.py"
        assert script_path.exists(), f"Script not found: {script_path}"

        exit_code, stdout, stderr = self._run_python_script(script_path)

        print(f"\n--- Rectangle Quickstart Output ---")
        print(f"Exit code: {exit_code}")
        if stdout:
            print(f"Stdout: {stdout[:500]}...")
        if stderr:
            print(f"Stderr: {stderr}")

        assert exit_code == 0, (
            f"Rectangle quickstart failed with exit code {exit_code}. Stderr: {stderr}"
        )
