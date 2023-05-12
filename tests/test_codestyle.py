"""Tests for code style."""
import os
from subprocess import run
from glob import glob
from pylint.lint import Run


class TestStyle:
    """Style test case."""

    def setup_class(self):
        """Setup."""
        project_path = os.path.split(os.path.dirname(__file__))[0]
        course_files = glob(os.path.join(project_path, "src", "*.py"))
        assert course_files, "No files to check!"
        pylint_results = Run(course_files, exit=False)
        self.style_result = pylint_results.linter.stats.global_note  # pylint: disable=attribute-defined-outside-init
        # evaluation =  https://github.com/PyCQA/pylint/issues/2399

    def test_20pc(self):
        """Test style >= 20%."""
        assert self.style_result >= 2.

    def test_40pc(self):
        """Test style >= 40%."""
        assert self.style_result >= 4.

    def test_60pc(self):
        """Test style >= 60%."""
        assert self.style_result >= 6.

    def test_80pc(self):
        """Test style >= 80%."""
        assert self.style_result >= 8.

    def test_90pc(self):
        """Test style >= 90%."""
        assert self.style_result >= 9.

def test_documentation():
    """Test documentation style."""
    project_path = os.path.split(os.path.dirname(__file__))[0]
    course_files = " ".join(glob(os.path.join(project_path, "src", "*.py")))
    cmd = rf"pydocstyle --select=D100,D102,D103,D419 {course_files}"
    res = run(cmd, shell=True, capture_output=True, check=False)
    missing_docs = len(res.stdout.splitlines()) / 2
    assert missing_docs == 0
