import subprocess
import shutil
from pathlib import Path
import tempfile
from typing import Tuple

def apply_fix_and_test(
    original_file: Path,
    fixed_code: str,
    tests_path: Path = None
) -> Tuple[bool, str]:
    """
    Applies fixed code and validates it.

    If tests_path is provided → run pytest
    If not → perform syntax validation
    """

    # -------- CASE 1: NO TEST FILE --------
    if tests_path is None:
        try:
            compile(fixed_code, filename=str(original_file), mode='exec')
            return True, "✅ Syntax is valid (No tests provided)"
        except Exception as e:
            return False, f"❌ Syntax Error:\n{str(e)}"

    # -------- CASE 2: TEST FILE EXISTS --------
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Copy all files from test directory safely
        try:
            for f in tests_path.parent.iterdir():
                if f.is_file():
                    shutil.copy(f, tmpdir / f.name)
        except Exception as e:
            return False, f"❌ Error copying test files: {str(e)}"

        # Write fixed code
        target = tmpdir / original_file.name
        target.write_text(fixed_code, encoding="utf-8")

        # Run pytest
        try:
            res = subprocess.run(
                ["pytest", "-q"],
                cwd=str(tmpdir),
                capture_output=True,
                text=True
            )

            success = (res.returncode == 0)
            output = res.stdout + "\n" + res.stderr

            return success, output

        except Exception as e:
            return False, f"❌ Pytest execution error: {str(e)}"