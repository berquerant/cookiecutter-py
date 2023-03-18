import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Union

import pytest
from cookiecutter.utils import rmtree


@contextmanager
def cd(p: Path):
    now = Path.cwd()
    try:
        os.chdir(str(p))
        yield
    finally:
        os.chdir(str(now))


@contextmanager
def bake(cookies, *args, **kwrags):
    r = cookies.bake(*args, **kwrags)
    try:
        yield r
    finally:
        rmtree(str(r.project_path))


def run(
    cmd: Union[str, list[str]], dir: Path, *args, **kwargs
) -> subprocess.CompletedProcess:
    with cd(dir):
        return subprocess.run(cmd, check=True, *args, **kwargs)


def check_result(result):
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == "python_project_template"
    project_path = result.project_path

    run(["pipenv", "install", "--dev"], project_path)
    scripts = ["check", "fmt", "test", "ci", "dev", "install", "dist"]
    for x in scripts:
        run(["pipenv", "run", x], project_path)


def test_bake_and_make_default(cookies):
    with bake(cookies) as result:
        check_result(result)


def test_bake_and_make_py311(cookies):
    context = {
        "python_version": "3.11",
        "black_target": "py311",
        "pytest_target": "py311",
    }
    with bake(cookies, extra_context=context) as result:
        check_result(result)
