import pytest
import subprocess

COVERAGE_THRESHOLD = 50
def test_code_coverage():
    result = subprocess.run(
        ["pytest", "--cov=taogod_terminal", "--ignore=tests/test_coverage.py", f"--cov-fail-under={COVERAGE_THRESHOLD}"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Coverage test failed:\n{result.stdout}\n{result.stderr}"
