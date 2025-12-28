import os
import subprocess
import sys
import unittest
import shutil
from pathlib import Path

class TestBuildHooks(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).parent.parent.absolute()
        self.sample_dir = self.project_root / "tests" / "sample_project"
        self.pre_marker = self.sample_dir / "pre_success.txt"
        self.post_marker = self.sample_dir / "post_success.txt"
        self.dist_dir = self.sample_dir / "dist"
        self.egg_info = self.sample_dir / "sample_project.egg-info"

        # Cleanup before run
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        for f in [self.pre_marker, self.post_marker]:
            if f.exists():
                f.unlink()
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        if self.egg_info.exists():
            shutil.rmtree(self.egg_info)

    def test_hooks_execution(self):
        """
        Verify that pre-build and post-build hooks are executed
        when building a project using build_meta_plus.
        """
        # Run build with PYTHONPATH pointing to our backend source
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root) + os.pathsep + env.get("PYTHONPATH", "")
        
        # --no-isolation is required to use the backend from the current environment/PYTHONPATH
        result = subprocess.run(
            [sys.executable, "-m", "build", "--no-isolation", "--wheel"],
            cwd=self.sample_dir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # If the build fails, print output for debugging
        if result.returncode != 0:
            print("\nSTDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        
        self.assertEqual(result.returncode, 0, "The build process failed.")
        
        # Check if marker files were created by the hooks
        self.assertTrue(self.pre_marker.exists(), "Pre-build hook (touch) did not execute.")
        self.assertTrue(self.post_marker.exists(), "Post-build hook (touch) did not execute.")

if __name__ == "__main__":
    unittest.main()
