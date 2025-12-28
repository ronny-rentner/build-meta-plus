import sys
import subprocess
from setuptools import build_meta
from setuptools.build_meta import *
from setuptools.config.pyprojecttoml import read_configuration

def _get_hooks():
    try:
        config = read_configuration("pyproject.toml")
        hooks = config.get("tool", {}).get("build_meta_plus", {})
        return hooks.get("pre-build", []), hooks.get("post-build", [])
    except Exception as e:
        print(f"[build_meta_plus] Warning: failed to read configuration: {e}")
        return [], []

def _run_hooks(hooks, phase):
    for cmd in hooks:
        print(f"[build_meta_plus] {phase}-build: {cmd}")
        subprocess.run(cmd, shell=True, check=True, stdout=sys.stdout, stderr=sys.stderr)

def build_editable(*args, **kwargs):
    pre, post = _get_hooks()
    _run_hooks(pre, "pre")
    result = build_meta.build_editable(*args, **kwargs)
    _run_hooks(post, "post")
    return result

def build_wheel(*args, **kwargs):
    pre, post = _get_hooks()
    _run_hooks(pre, "pre")
    result = build_meta.build_wheel(*args, **kwargs)
    _run_hooks(post, "post")
    return result

def build_sdist(*args, **kwargs):
    pre, post = _get_hooks()
    _run_hooks(pre, "pre")
    result = build_meta.build_sdist(*args, **kwargs)
    _run_hooks(post, "post")
    return result
